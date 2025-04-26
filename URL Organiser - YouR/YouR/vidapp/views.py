from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import VideoBookmark, Tag
from .forms import RegisterForm, VideoBookmarkForm, SearchForm
import requests
from bs4 import BeautifulSoup
import re
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.



def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send welcome email
            # Send welcome email
            current_site = get_current_site(request)
            site_url = f"http://{current_site.domain}"
            subject = 'Welcome to YouR!'
            message = render_to_string('vidapp/email_template/welcome_email.html', {
                'user': user,
                'site_url': site_url,
            })
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
            email.content_subtype = 'html'
            email.send()

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'vidapp/register.html', {'form': form})


def home(request):
    # Public landing page
    return render(request, 'vidapp/home.html')

@login_required
def dashboard(request):
    """User dashboard showing recent bookmarks"""
    recent_bookmarks = VideoBookmark.objects.filter(user=request.user).order_by('-created_at')[:5]
    popular_tags = Tag.objects.filter(videos__user=request.user).distinct()
    
    context = {
        'recent_bookmarks': recent_bookmarks,
        'popular_tags': popular_tags,
    }
    return render(request, 'vidapp/dashboard.html', context)

@login_required
def add_video(request):
    """Add a new video bookmark"""
    if request.method == 'POST':
        form = VideoBookmarkForm(request.POST)
        if form.is_valid():
            # Attempt to fetch title and thumbnail if not provided
            new_bookmark = form.save(commit=False, user=request.user)
            
            # If title is not provided, try to fetch it
            if not new_bookmark.title or not new_bookmark.thumbnail_url:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(new_bookmark.url, headers=headers, timeout=5)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Get title if not provided
                        if not new_bookmark.title:
                            title_tag = soup.find('title')
                            if title_tag:
                                new_bookmark.title = title_tag.text.strip()
                        
                        # Get thumbnail if not provided
                        if not new_bookmark.thumbnail_url:
                            og_image = soup.find('meta', property='og:image')
                            if og_image and og_image.get('content'):
                                new_bookmark.thumbnail_url = og_image.get('content')
                except:
                    # If fetching fails, continue without it
                    pass
            
            form.save()
            messages.success(request, 'Video bookmark added successfully!')
            return redirect('video_list')
    else:
        form = VideoBookmarkForm()
    
    return render(request, 'vidapp/add_video.html', {'form': form})

@login_required
def video_list(request):
    """Display all user's video bookmarks with search functionality"""
    bookmarks = VideoBookmark.objects.filter(user=request.user)
    form = SearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        tags = form.cleaned_data.get('tags')
        source = form.cleaned_data.get('source')
        
        if query:
            bookmarks = bookmarks.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if tags:
            bookmarks = bookmarks.filter(tags__in=tags).distinct()
        
        if source:
            # Filter by source based on URL patterns
            if source == 'YouTube':
                bookmarks = bookmarks.filter(Q(url__icontains='youtube') | Q(url__icontains='youtu.be'))
            elif source == 'Instagram':
                bookmarks = bookmarks.filter(url__icontains='instagram')
            elif source == 'LinkedIn':
                bookmarks = bookmarks.filter(url__icontains='linkedin')
            elif source == 'X':
                bookmarks = bookmarks.filter(Q(url__icontains='x.com'))
            elif source == 'Threads':
                bookmarks = bookmarks.filter(url__icontains='threads')
            elif source == 'Vimeo':
                bookmarks = bookmarks.filter(url__icontains='vimeo')
            elif source == 'Other':
                bookmarks = bookmarks.exclude(
                    Q(url__icontains='youtube') | 
                    Q(url__icontains='youtu.be') |
                    Q(url__icontains='instagram') |
                    Q(url__icontains='linkedin') |
                    Q(url__icontains='x.com') |
                    Q(url__icontains='threads') |
                    Q(url__icontains='vimeo')
                )
    
    context = {
        'bookmarks': bookmarks,
        'form': form,
    }
    return render(request, 'vidapp/video_list.html', context)

@login_required
def video_detail(request, pk):
    """Display details of a single video bookmark"""
    bookmark = get_object_or_404(VideoBookmark, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Handle deletion
        if 'delete' in request.POST:
            bookmark.delete()
            messages.success(request, 'Video bookmark deleted successfully!')
            return redirect('video_list')
    
    return render(request, 'vidapp/video_detail.html', {'bookmark': bookmark})

@login_required
def edit_video(request, pk):
    """Edit an existing video bookmark"""
    bookmark = get_object_or_404(VideoBookmark, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = VideoBookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Video bookmark updated successfully!')
            return redirect('video_detail', pk=bookmark.pk)
    else:
        # Prepare initial tag input for the form
        initial_data = {
            'tags_input': ', '.join([tag.name for tag in bookmark.tags.all()])
        }
        form = VideoBookmarkForm(instance=bookmark, initial=initial_data)
    
    return render(request, 'vidapp/edit_video.html', {'form': form, 'bookmark': bookmark})
