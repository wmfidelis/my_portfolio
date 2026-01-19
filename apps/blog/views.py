from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, PostSearchForm

def post_list(request):
    """Display list of published posts with search and filtering"""
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    search_form = PostSearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )
        
        if category:
            posts = posts.filter(category=category)
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get popular posts (most viewed)
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    
    # Get all categories with post count
    categories = Category.objects.annotate(post_count=Count('posts', filter=Q(posts__status='published')))
    
    # Get all tags
    tags = Tag.objects.annotate(post_count=Count('posts', filter=Q(posts__status='published')))
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Display single post with comments"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments'),
        slug=slug,
        status='published'
    )
    
    # Increment view count
    post.increment_views()
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True, parent=None).select_related('author').prefetch_related('replies')
    
    # Handle comment form submission
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                
                # Handle reply to comment
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent = get_object_or_404(Comment, id=parent_id)
                
                comment.save()
                messages.success(request, 'Comment posted successfully!')
                return redirect('blog:post_detail', slug=post.slug)
        else:
            messages.warning(request, 'Please login to post a comment.')
            return redirect('login')
    else:
        comment_form = CommentForm()
    
    # Get related posts
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    """Create new blog post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, f'Post "{post.title}" created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Create New Post'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_update(request, slug):
    """Update existing blog post"""
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is author or staff
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f'Post "{post.title}" updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'title': 'Edit Post'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_delete(request, slug):
    """Delete blog post"""
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is author or staff
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" deleted successfully!')
        return redirect('blog:post_list')
    
    context = {
        'post': post
    }
    return render(request, 'blog/post_confirm_delete.html', context)


def category_posts(request, slug):
    """Display posts in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').select_related('author')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """Display posts with a specific tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published').select_related('author')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_posts.html', context)


@login_required
def comment_delete(request, pk):
    """Delete a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check if user is comment author or staff
    if comment.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('blog:post_detail', slug=comment.post.slug)
    
    post_slug = comment.post.slug
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('blog:post_detail', slug=post_slug)