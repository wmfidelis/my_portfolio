from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Skill, ContactMessage
from .forms import ContactForm, EmailSignupForm 
from .utils import send_email_async


def index(request):
    """Homepage view"""
    skills = Skill.objects.all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    context = {
        'skills_by_category': skills_by_category,
    }
    return render(request, 'portfolio_site/index.html', context)


def projects(request):
    """Projects listing view"""
    all_projects = Project.objects.all()
    
    context = {
        'projects': all_projects,
    }
    return render(request, 'portfolio_site/projects.html', context)


def project_detail(request, pk):
    """Project detail view"""
    project = get_object_or_404(Project, pk=pk)
    
    context = {
        'project': project,
    }
    return render(request, 'portfolio_site/project_detail.html', context)


def contact(request):
    """Contact form view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification (optional)
            if settings.EMAIL_HOST_USER:
                try:
                    send_email_async(
                        subject=f"New Contact Form: {contact_message.subject}",
                        message=f"From: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.EMAIL_HOST_USER],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Email error: {e}")
            
            messages.success(
                request, 
                'Thank you for your message! I will get back to you soon.'
            )
            return redirect('portfolio_site:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'portfolio_site/contact.html', context)



def signup(request):
    if request.user.is_authenticated:
        return redirect('portfolio_site:index')
    
    if request.method == 'POST':
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('portfolio_site:index')
    else:
        form = EmailSignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})
