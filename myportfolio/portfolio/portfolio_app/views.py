from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tech, Project, Certificate, CV
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

# Create your views here.

def index(request):
    techs = Tech.objects.prefetch_related('skill_set').order_by('-display_priority')
    
    query = request.GET.get('q')
    if query:
        posts_list = Project.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(tag1__icontains=query) |
            Q(tag2__icontains=query) |
            Q(tag3__icontains=query) |
            Q(tag4__icontains=query) |
            Q(tag5__icontains=query)
        ).distinct().order_by('-display_priority')
    else:
        posts_list = Project.objects.order_by('-display_priority')
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    certificates = Certificate.objects.all()  # Fetch all certificates
    latest_cv = CV.objects.order_by('-uploaded_at').first()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'techs': techs,
        'certificates': certificates,
        'latest_cv': latest_cv,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('portfolio_app/index.html', context, request=request)
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'num_pages': paginator.num_pages,
        })

    return render(request, 'portfolio_app/index.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    
    context = {
        'project': project,
    }
    
    return render(request, 'portfolio_app/detail.html', context)

def send_contact_email(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    if all([name, email, subject, message]):
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        try:
            send_mail(
                subject=f"Contact Form from Portfolio: {subject}",
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