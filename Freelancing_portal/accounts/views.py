from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .models import Freelancer, Business

@login_required
def profile_view(request):
    return render(request, "jobs/profile.html")

# @login_required
# def create_freelancer(request):
#     user = request.user
#     if request.method == 'POST':
#         Freelancer.objects.create(user=user, tagline=request.POST.get('tagline', ''), bio=request.POST.get('bio', ''))
#         user.user_type = 'freelancer'
#         user.save()
#         return redirect('freelancer-dashboard')
#     return render(request, 'jobs/freelancer_form.html')


# @login_required
# def create_business(request):
#     user = request.user
#     if request.method == 'POST':
#         Business.objects.create(user=user, bio=request.POST.get('bio', ''))
#         user.user_type = 'business'
#         user.save()
#         return redirect('business-dashboard')
#     return render(request, 'jobs/business_form.html')
