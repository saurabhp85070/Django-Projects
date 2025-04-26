from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, SigninForm
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UpdateProfileForm
from django.core.files.storage import default_storage
import os
from django.conf import settings
from .models import UserProfile
from blog_app.models import BlogPost, SavedPost
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site



# Create your views here.

# SIGNUP HANDLING
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            verification_link = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token_generator.make_token(user)})}"
            subject = 'Activate your Ullekh account'
            message = render_to_string('user_app/email_template/verification_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'Registration successful. Please check your email to verify your account.')
            return redirect('index')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'user_app/signup.html', context)

# ACCOUNT ACTIVATION HANDLING
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Your account is now active.')

        # Send welcome email
        current_site = get_current_site(request)
        site_url = f"http://{current_site.domain}"
        subject = 'Welcome to Ullekh!'
        message = render_to_string('user_app/email_template/welcome_email.html', {
            'user': user,
            'site_url': site_url,
        })
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
        email.content_subtype = 'html'
        email.send()

        return redirect('index')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('signup')
    
# SIGNIN HANDLING
def signin(request):
    if request.user.is_authenticated: # preventing logged in user to signin
        return redirect('index')
    
    if request.method == "POST":
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('index')
    else:
        form = SigninForm()
    context = {
        'form': form,
    }
    return render(request, 'user_app/signin.html', context)

# LOGOUT HANDLING
@login_required
@require_http_methods(["GET", "POST"])
def signout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout successful")
        return redirect('index')
    else:
        messages.error(request, "Invalid logout attempt. Please use the logout button.")
        return redirect('index')  # or redirect to any other appropriate page

# CHANGE PASSWORD HANDLING
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password updated successfully')
            return redirect('account')
    else:
        form = ChangePasswordForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'user_app/changePswd.html', context)

# USER ACCOUNT HANDLING
@login_required
def user_account(request):
    user_account = request.user.userprofile
    
    # Fetch user's blogs, ordered by creation date (most recent first)
    user_blogs = BlogPost.objects.filter(author=user_account).order_by('-created_at')
    
    # Fetch saved posts, ordered by save date (most recent first)
    saved_posts = SavedPost.objects.filter(user=user_account).select_related('post').order_by('-saved_at')
    
    # Get follower and following counts
    follower_count = user_account.followers.count()
    following_count = user_account.following.count()
    
    # Get following users
    following_users = user_account.following.all()
    
    context = {
        'user_account': user_account,
        'user_blogs': user_blogs,
        'saved_posts': saved_posts,
        'follower_count': follower_count,
        'following_count': following_count,
        'following_users': following_users,
    }
    
    return render(request, 'user_app/account.html', context)

# UPDATE ACCOUNT HANDLING
@login_required
def update_user_account(request):
    userprofile = request.user.userprofile
    user = request.user
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            # Update User model fields
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            # Save UserProfile fields
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
        }
        form = UpdateProfileForm(instance=userprofile, initial=initial_data)
    context = {
        'form': form,
    }
    return render(request, 'user_app/update.html', context)

# DELETE ACCOUNT HANDLING
@login_required
def delete_user_account(request):
    profile = request.user.userprofile
    user = request.user
    
    if request.method == 'POST':
        # Delete all blog images associated with the user
        user_blogs = BlogPost.objects.filter(author=profile)
        for blog in user_blogs:
            if blog.image and default_storage.exists(blog.image.name):
                default_storage.delete(blog.image.name)
            blog.delete()

        # Delete profile picture if it exists
        if profile.profile_pic:
            profile_pic_path = profile.profile_pic.path
            if default_storage.exists(profile_pic_path):
                default_storage.delete(profile_pic_path)
        
        # Delete profile and user
        profile.delete()
        user.delete()
        messages.success(request, 'Account and all associated data deleted successfully')
        return redirect('index')
    
    return render(request, 'user_app/delete.html')


# FORGOT PASSWORD HANDLING
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "user_app/email_template/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Ullekh',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    html_content = render_to_string(email_template_name, c)
                    text_content = strip_tags(html_content)
                    
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
            # Always redirect to password_reset_done, even if the email doesn't exist
            return redirect("password_reset_done")
    else:
        password_reset_form = PasswordResetForm()
    
    context = {
        "form": password_reset_form,
    }
    return render(request, "user_app/password_reset.html", context)