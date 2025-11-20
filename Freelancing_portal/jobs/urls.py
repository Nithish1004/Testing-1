from django.urls import path
from accounts.views import profile_view
from .views import BusinessCreateView, FreelancerCreateView, FreelancerDetailView, FreelancerListView
from .views import handle_login, job_list, post_job, apply_job, my_job_applicants, my_applied_jobs, manage_applications

urlpatterns = [
    # path('profile/', profile_view, name='profile'),
    path('', FreelancerListView.as_view(), name='freelancer-list'),
    path('jobs/', job_list, name='job-list'),
    path('my-jobs/', post_job, name='post-jobs'),
    path('apply/<int:job_id>/', apply_job, name='apply-job'),
    path('account-setup/', handle_login, name='handle-login'),
    # path('developer/<int:pk>/', FreelancerDetailView.as_view(), name='freelancer-detail'),
    path('freelancer/<int:pk>/', FreelancerDetailView.as_view(), name='freelancer-detail'),
    path('developer/create/', FreelancerCreateView.as_view(), name="freelancer-create"),
    path('business/create/', BusinessCreateView.as_view(), name="business-create"),
    # path('apply/<int:job_id>/', apply_job, name='apply-job'),
    # path('applications/<int:job_id>/', job_applications, name='job-applications'),
    path('apply/<int:job_id>/', apply_job, name='apply-job'),
    # path('applicants/<int:job_id>/', job_applicants, name='job-applicants'),
    path('my-applicants/', my_job_applicants, name='my-job-applicants'),
    path('applicants/<int:job_id>/', manage_applications, name='manage-applications'),
    path('my-applied-jobs/', my_applied_jobs, name='my-applied-jobs'),
]

