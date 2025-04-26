from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NewsletterSubscription
from django.views.decorators.http import require_POST

# Create your views here.


@require_POST
def subscribe_newsletter(request):
    email = request.POST.get('email')
    if email:
        if NewsletterSubscription.objects.filter(email=email).exists():
            messages.info(request, "You're already subscribed to our newsletter.")
        else:
            NewsletterSubscription.objects.create(email=email)
            messages.success(request, "Thank you for subscribing to our newsletter!")
    else:
        messages.error(request, "Please provide a valid email address.")
    return redirect('index')