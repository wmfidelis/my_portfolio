from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from django.core.cache import cache
from datetime import datetime, timedelta
import requests
from .models import (DailyCheckIn, Affirmation, AffirmationCategory, GratitudeEntry, 
                     MeditationSession, Resource, CommunityPost, CommunityPostLike)
from .forms import DailyCheckInForm, GratitudeEntryForm, MeditationSessionForm, CommunityPostForm

def get_daily_affirmation():
    """Get affirmation from API or database"""
    # Try cache first
    cached_affirmation = cache.get('daily_affirmation')
    if cached_affirmation:
        return cached_affirmation
    
    # Try API
    try:
        response = requests.get('https://www.affirmations.dev/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            affirmation = data.get('affirmation', '')
            # Cache for 1 hour
            cache.set('daily_affirmation', affirmation, 3600)
            return affirmation
    except:
        pass
    
    # Fallback to database
    affirmation = Affirmation.objects.filter(is_active=True).order_by('?').first()
    if affirmation:
        return affirmation.text
    
    return "You are worthy of love, peace, and happiness. 🌟"


@login_required
def index(request):
    """Hope & Healing Journey homepage/dashboard"""
    today = timezone.now().date()
    
    # Get or create today's check-in
    checkin, created = DailyCheckIn.objects.get_or_create(
        user=request.user,
        date=today
    )
    
    # Get daily affirmation
    daily_affirmation = get_daily_affirmation()
    
    # Get recent entries
    recent_gratitude = GratitudeEntry.objects.filter(user=request.user)[:3]
    recent_sessions = MeditationSession.objects.filter(user=request.user)[:5]
    
    # Get stats for last 7 days
    week_ago = today - timedelta(days=7)
    weekly_checkins = DailyCheckIn.objects.filter(
        user=request.user,
        date__gte=week_ago
    )
    
    days_checked_in = weekly_checkins.count()
    total_meditation_minutes = MeditationSession.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).aggregate(total=Count('duration_minutes'))['total'] or 0
    
    # Crisis support resources
    crisis_resources = Resource.objects.filter(is_crisis_support=True)[:3]
    
    context = {
        'checkin': checkin,
        'daily_affirmation': daily_affirmation,
        'recent_gratitude': recent_gratitude,
        'recent_sessions': recent_sessions,
        'days_checked_in': days_checked_in,
        'total_meditation_minutes': total_meditation_minutes,
        'crisis_resources': crisis_resources,
    }
    return render(request, 'hope_healing/index.html', context)


@login_required
def daily_checkin(request):
    """Daily mood and practice check-in"""
    today = timezone.localdate()

    checkin, created = DailyCheckIn.objects.get_or_create(
        user=request.user,
        date=today
    )

    if request.method == 'POST':
        form = DailyCheckInForm(request.POST, instance=checkin)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                '🙏 Check-in saved — thank you for showing up for yourself'
            )
            return redirect('hope_healing:daily_checkin')
    else:
        form = DailyCheckInForm(instance=checkin)

    return render(
        request,
        'hope_healing/daily_checkin.html',
        {
            'form': form,
            'checkin': checkin,
        }
    )



@login_required
def affirmations(request):
    """Browse affirmations by category"""
    categories = AffirmationCategory.objects.annotate(
        affirmation_count=Count('affirmations')
    )
    
    selected_category = request.GET.get('category')
    if selected_category:
        affirmations_list = Affirmation.objects.filter(
            category_id=selected_category,
            is_active=True
        )
    else:
        affirmations_list = Affirmation.objects.filter(is_active=True)[:20]
    
    # Get random affirmation
    random_affirmation = get_daily_affirmation()
    
    context = {
        'categories': categories,
        'affirmations_list': affirmations_list,
        'random_affirmation': random_affirmation,
        'selected_category': selected_category,
    }
    return render(request, 'hope_healing/affirmations.html', context)


@login_required
def gratitude_journal(request):
    """Gratitude journal entries - one per day"""
    today = timezone.now().date()

    # Try to get today's entry safely
    entry, created = GratitudeEntry.objects.get_or_create(
    user=request.user,
    date=today,
)

    if request.method == 'POST':
        form = GratitudeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, '🙏 Gratitude entry saved! Keep nurturing gratitude.')
            return redirect('hope_healing:gratitude_journal')
    else:
        form = GratitudeEntryForm(instance=entry)

    # Show all entries
    entries = GratitudeEntry.objects.filter(user=request.user).order_by('date')

    context = {
        'form': form,
        'entries': entries,
        'today': timezone.now().date(),
        
    }
    return render(request, 'hope_healing/gratitude_journal.html', context)


@login_required
def meditation_timer(request):
    """Meditation/prayer timer and session logging"""
    # Try to get today's session so user can edit notes if they already exist
    today = timezone.now().date()
    session, created = MeditationSession.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'duration_minutes': 0, 'session_type': 'meditation'}  # adjust default as needed
    )

    if request.method == 'POST':
        form = MeditationSessionForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()  # ✅ This saves notes too
            messages.success(
                request,
                f'🧘 {session.get_session_type_display()} session logged with notes!'
            )
            return redirect('hope_healing:meditation_timer')
    else:
        form = MeditationSessionForm(instance=session)

    recent_sessions = MeditationSession.objects.filter(user=request.user).order_by('-date')[:10]
    total_minutes = MeditationSession.objects.filter(user=request.user).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0

    context = {
        'form': form,
        'recent_sessions': recent_sessions,
        'total_minutes': total_minutes,
        'session': session,  # optional if you want to pre-fill notes
    }
    return render(request, 'hope_healing/meditation_timer.html', context)



@login_required
def progress_dashboard(request):
    """Progress tracking dashboard"""
    # Get date range (last 30 days)
    today = timezone.now().date()
    month_ago = today - timedelta(days=30)
    
    # Daily check-ins
    checkins = DailyCheckIn.objects.filter(
        user=request.user,
        date__gte=month_ago
    ).order_by('date')
    
    # Meditation sessions
    sessions = MeditationSession.objects.filter(
        user=request.user,
        date__gte=month_ago
    )
    
    # Calculate stats
    total_checkins = checkins.count()
    total_meditation_time = sessions.aggregate(total=Count('duration_minutes'))['total'] or 0
    total_gratitude_entries = GratitudeEntry.objects.filter(
        user=request.user,
        date__gte=month_ago
    ).count()
    
    # Mood trends
    mood_data = []
    for checkin in checkins:
        if checkin.morning_mood:
            mood_data.append({
                'date': checkin.date,
                'mood': checkin.morning_mood,
                'type': 'morning'
            })
    
    context = {
        'total_checkins': total_checkins,
        'total_meditation_time': total_meditation_time,
        'total_gratitude_entries': total_gratitude_entries,
        'checkins': checkins,
        'sessions': sessions,
        'mood_data': mood_data,
    }
    return render(request, 'hope_healing/progress_dashboard.html', context)


def resources(request):
    """Mental health and spiritual resources"""
    crisis_resources = Resource.objects.filter(is_crisis_support=True)
    featured_resources = Resource.objects.filter(is_featured=True, is_crisis_support=False)
    other_resources = Resource.objects.filter(is_featured=False, is_crisis_support=False)
    
    context = {
        'crisis_resources': crisis_resources,
        'featured_resources': featured_resources,
        'other_resources': other_resources,
    }
    return render(request, 'hope_healing/resources.html', context)


@login_required
def community(request):
    """Community encouragement board"""
    if request.method == 'POST':
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '💙 Your encouragement has been shared!')
            return redirect('hope_healing:community')
    else:
        form = CommunityPostForm()
    
    posts = CommunityPost.objects.filter(is_approved=True)
    
    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'hope_healing/community.html', context)


@login_required
def toggle_like(request, post_id):
    """Toggle like on community post"""
    post = get_object_or_404(CommunityPost, id=post_id)
    
    like, created = CommunityPostLike.objects.get_or_create(
        user=request.user,
        post=post
    )
    
    if not created:
        like.delete()
        post.likes_count -= 1
    else:
        post.likes_count += 1
    
    post.save()
    return redirect('hope_healing:community')