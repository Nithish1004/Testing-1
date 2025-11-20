from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from jobs.forms import JobForm
from django.contrib import messages
from .models import Freelancer, Business


class FreelancerListView(ListView):
    model = Freelancer

class FreelancerDetailView(LoginRequiredMixin, DetailView):
    model = Freelancer
    # template 'freelancer_detail.html'

# def freelancer_detail(request, pk):
#     freelancer = Freelancer.objects.get(pk=pk) #get_object_or_404
#     context = {
#         "objects": freelancer
#     }
#     return render(request, 'jobs/freelancer_detail/html', context)

class FreelancerCreateView(LoginRequiredMixin, CreateView):
    model = Freelancer
    fields = ['name', 'profile_pic', 'tagline', 'bio', 'website']
    success_url = reverse_lazy('freelancer-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(FreelancerCreateView, self).form_valid(form)

class BusinessCreateView(LoginRequiredMixin, CreateView):
    model = Business
    fields = ['name', 'profile_pic', 'bio']
    success_url = reverse_lazy('freelancer-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BusinessCreateView, self).form_valid(form)

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['title', 'description', 'skills', 'budget']
    success_url = reverse_lazy('freelancer-list')

    def dispatch(self, request, *args, **kwargs):
        # Prevent freelancers from posting jobs
        if request.user.user_type != 'business':
            messages.error(request, "Only business accounts can post jobs.")
            return redirect('freelancer-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@login_required
def handle_login(request):
    user = request.user

    if user.get_freelancer() or user.get_business():
        return redirect('freelancer-list')

    if request.method == 'POST':
        account_type = request.POST.get('account_type')

        if account_type == 'freelancer':
            user.user_type = 'freelancer'
            user.save()
            return redirect('freelancer-create')

        elif account_type == 'business':
            user.user_type = 'business'
            user.save()
            return redirect('business-create')

    return render(request, 'jobs/choose_account.html')

@login_required(login_url='account_login')
def job_list(request):
    jobs = Job.objects.all()
    applied_jobs = []

    if request.user.is_authenticated and hasattr(request.user, 'freelancer'):
        freelancer = request.user.freelancer
        # Get all job IDs the freelancer has applied to
        applied_jobs = [app.job.id for app in freelancer.application_set.all()]

    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'applied_jobs': applied_jobs})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Ensure the user is a freelancer
    try:
        freelancer = request.user.freelancer
    except:
        messages.error(request, "Only freelancers can apply for jobs.")
        return redirect('job-list')

    # Check if already applied
    if Application.objects.filter(job=job, freelancer=freelancer).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect('job-list')

    # Create application
    Application.objects.create(job=job, freelancer=freelancer)
    messages.success(request, "You applied successfully!")
    return redirect('job-list')

@login_required
def post_job(request):
    try:
        business = request.user.business  # get the Business profile
    except Business.DoesNotExist:
        messages.error(request, "You must create a Business profile first.")
        return redirect('business-create')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.business = business  # assign the correct Business instance
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('job-list')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})
        
@login_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only allow the business owner to view applications
    if job.business.owner != request.user:
        messages.error(request, "You are not authorized to view applications for this job.")
        return redirect('job-list')

    applications = job.applications.all()  # thanks to related_name
    return render(request, 'jobs/job_applications.html', {'job': job, 'applications': applications})

@login_required
def my_job_applicants(request):
    try:
        business = request.user.business
    except:
        messages.error(request, "You must have a Business profile to view applicants.")
        return redirect('job-list')

    jobs = Job.objects.filter(business=business)
    return render(request, 'jobs/my_job_applicants.html', {'jobs': jobs})

@login_required
def manage_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Ensure the user is the business owner
    if job.business.owner != request.user:
        messages.error(request, "You are not authorized.")
        return redirect('job-list')

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        action = request.POST.get('action')  # 'accept' or 'reject'
        app = get_object_or_404(job.applications, id=app_id)

        if action == 'accept':
            app.status = 'accepted'
        elif action == 'reject':
            app.status = 'rejected'
        app.save()
        messages.success(request, f"{app.freelancer.name} has been {app.status}.")
        return redirect('manage-applications', job_id=job.id)

    applications = job.applications.all()
    return render(request, 'jobs/manage_applications.html', {'job': job, 'applications': applications})

@login_required
def my_applied_jobs(request):
    try:
        freelancer = request.user.freelancer
    except:
        messages.error(request, "Only freelancers can view this page.")
        return redirect('job-list')

    applications = freelancer.application_set.select_related('job').all()

    return render(request, 'jobs/my_applied_jobs.html', {'applications': applications})


