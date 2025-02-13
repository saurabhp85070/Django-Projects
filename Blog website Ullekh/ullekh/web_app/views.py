from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from blog_app.models import BlogPost
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from .models import Faq
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

# INDEX PAGE HANDLING
def index(request):
    query = request.GET.get('q')
    if query:
        posts_list = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(author__user__last_name__icontains=query)
        ).distinct().order_by('-created_at')
    else:
        posts_list = BlogPost.objects.order_by('-created_at')
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    faqs = Faq.objects.all() # get all FAQ
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'faqs': faqs,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('web_app/index.html', context, request=request)
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'num_pages': paginator.num_pages,
        })

    return render(request, 'web_app/index.html', context)


# CONTACT US PAGE HANDLING
@require_POST
def send_contact_email(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    if all([name, email, subject, message]):
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        try:
            send_mail(
                subject=f"Contact Form: {subject}",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "An error occurred while sending your message. Please try again later.")
    else:
        messages.error(request, "Please fill in all fields.")

    return redirect('index')

# PRIVACY POLICY PAGE HANDLING
def privacy(request):
    context = {
        'domain': get_current_site(request).domain,
        'protocol': 'http'
    }
    return render(request, 'web_app/privacy.html', context)

# TERMS OF USE PAGE HANDLING
def terms(request):
    context = {
        'domain': get_current_site(request).domain,
        'protocol': 'http'
    }
    return render(request, 'web_app/terms.html', context)