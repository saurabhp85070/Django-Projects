from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost, BlogComment, SavedPost
from .forms import BlogPostForm
from .models import UserProfile
from django.contrib import messages
from django.db.models import Prefetch
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse, JsonResponse

from .utils import generate_pdf


# Create your views here.

# CREATE BLOG PAGE HANDLING
@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user.userprofile
            blog_post.save()
            form.save_categories(blog_post)
            messages.success(request, "Your blog created successfully")
            return redirect('detailblog', post_id=blog_post.post_id)
    else:
        form = BlogPostForm()
    context = {
        'form': form,
        'is_update': False,  # This indicates it's a create operation
    }
    return render(request, 'blog_app/create.html', context)

# DETAIL PAGE HANDLING: COMMENT, REPLY, EDIT, DELETE, SAVE
@login_required
def detail_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, post_id=post_id)
    recent_posts = BlogPost.objects.exclude(post_id=post_id).order_by('-created_at')[:5]
    comments = BlogComment.objects.filter(post=post, parent=None).order_by('-created_at')
    
    comments = comments.prefetch_related(
        Prefetch('blogcomment_set', 
                queryset=BlogComment.objects.order_by('created_at'),
                to_attr='replies')
    )
    
    total_comments = BlogComment.objects.filter(post=post).count()
    is_saved = SavedPost.objects.filter(user=request.user.userprofile, post=post).exists()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_comment':
            comment_text = request.POST.get('comment')
            user = request.user.userprofile
            parentSno = request.POST.get('parentSno')
            
            if parentSno == "":
                comment = BlogComment(comment=comment_text, user=user, post=post)
                comment.save()
                messages.success(request, 'Your comment has been posted successfully')
            else:
                parent = BlogComment.objects.get(sno=parentSno)
                comment = BlogComment(comment=comment_text, user=user, post=post, parent=parent)
                comment.save()
                messages.success(request, 'Your reply has been posted successfully')
        
        elif action == 'edit_comment':
            comment_id = request.POST.get('comment_id')
            new_comment_text = request.POST.get('comment')
            comment = get_object_or_404(BlogComment, sno=comment_id)
            
            if request.user.userprofile == comment.user:
                comment.comment = new_comment_text
                comment.save()
                messages.success(request, 'Your comment has been updated successfully')
            else:
                messages.error(request, 'You are not authorized to edit this comment')
        
        # In the delete_comment action
        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(BlogComment, sno=comment_id)
            
            if request.user.userprofile == comment.user:
                def count_replies(comment):
                    count = 1
                    for reply in comment.blogcomment_set.all():
                        count += count_replies(reply)
                    return count

                comments_to_delete = count_replies(comment)
                
                comment.delete()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'deleted_count': comments_to_delete,
                        'message': 'Your comment has been deleted successfully'  # Add this line
                    })
                messages.success(request, 'Your comment has been deleted successfully')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False, 
                        'error': 'You are not authorized to delete this comment'
                    }, status=403)
                messages.error(request, 'You are not authorized to delete this comment')
        
        elif action == 'toggle_save':
            user = request.user.userprofile
            saved_post, created = SavedPost.objects.get_or_create(user=user, post=post)
            
            if not created:
                saved_post.delete()
                is_saved = False
            else:
                is_saved = True
            
            return JsonResponse({'is_saved': is_saved})
        
        # Refresh comments after any action
        comments = BlogComment.objects.filter(post=post, parent=None).order_by('-created_at')
        comments = comments.prefetch_related(
            Prefetch('blogcomment_set', 
                    queryset=BlogComment.objects.order_by('created_at'),
                    to_attr='replies')
        )
        total_comments = BlogComment.objects.filter(post=post).count()
        
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = {
                'post': post,
                'recent_posts': recent_posts,
                'comments': comments,
                'total_comments': total_comments,
                'is_saved': is_saved,
            }
            html = render_to_string('blog_app/detail.html', context, request=request)
            return HttpResponse(html)
        else:
            # For non-AJAX requests, redirect with anchor
            redirect_url = reverse('detailblog', kwargs={'post_id': post_id})
            if action == 'add_comment' or action == 'edit_comment':
                redirect_url += f'#comment-{comment.sno}'
            return redirect(redirect_url)

    context = {
        'post': post,
        'recent_posts': recent_posts,
        'comments': comments,
        'total_comments': total_comments,
        'is_saved': is_saved,
    }
    return render(request, 'blog_app/detail.html', context)



# UPDATE PAGE HANDLING
@login_required
def update_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, post_id=post_id)
    
    # Check if the current user is the author
    if request.user.userprofile != post.author:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('detailblog', post_id=post.post_id)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your blog updated successfully')
            return redirect('detailblog', post_id=post.post_id)
    else:
        form = BlogPostForm(instance=post)
    context = {
        'form': form,
        'is_update': True,  # This indicates it's an update operation
    }
    return render(request, 'blog_app/create.html', context)

# DELETE PAGE HANDLING
@login_required
def delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, post_id=post_id)
    
    # Check if the current user is the author
    if request.user.userprofile != post.author:
        messages.error(request, "You don't have permission to delete this post.")
        return redirect('detailblog', post_id=post.post_id)
    
    if request.method == 'POST':
        # Delete blog image if it exists
        if post.image and default_storage.exists(post.image.name):
            default_storage.delete(post.image.name)
        
        post.delete()
        messages.success(request, 'Your blog deleted successfully')
        return redirect('index')
    
    next_url = request.GET.get('next', 'account')
    context = {
        'post': post,
        'next_url': next_url,
    }
    return render(request, 'blog_app/delete.html', context)

# AUTHOR PROFILE PAGE HANDLING
@login_required
def author_profile(request, pk):
    author_profile = get_object_or_404(UserProfile, profile_id=pk)
    author_blogs = BlogPost.objects.filter(author=author_profile).order_by('-created_at')
    is_following = request.user in author_profile.followers.all()
    follower_count = author_profile.get_follower_count()
    following_users = author_profile.following.all()
    following_count = len(following_users)

    if request.method == 'POST':
        if 'follow' in request.POST:
            author_profile.followers.add(request.user)
            request.user.userprofile.following.add(author_profile.user)
            is_following = True
            follower_count += 1
            following_count = author_profile.get_following_count()
        elif 'unfollow' in request.POST:
            author_profile.followers.remove(request.user)
            request.user.userprofile.following.remove(author_profile.user)
            is_following = False
            follower_count -= 1
            following_count = author_profile.get_following_count()


    context = {
        'author_profile': author_profile,
        'author_blogs': author_blogs,
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
        'following_users': following_users,
    }
    return render(request, 'blog_app/profile.html', context)


@login_required
def download_pdf(request, post_id):
    post = get_object_or_404(BlogPost, post_id=post_id)
    pdf = generate_pdf(post)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{post.title}.pdf"'
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)