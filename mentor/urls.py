from django.urls import path
from . import views

urlpatterns = [
    path('mentor_dashboard/',views.mentor_dashboard,name="mentor_dashboard"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('mentor_change_password/',views.mentor_change_password,name="mentor_change_password"),
    path('m_terms/',views.m_terms,name="m_terms"),
    path('update-terms-status/', views.update_terms_status, name='update_terms_status'),
    path('m_working_on/',views.m_working_on,name="m_working_on"),
    path('get-participant-details/<int:user_id>/', views.get_participant_details, name='get_participant_details'),
    path('create_mentor_profile/',views.create_mentor_profile,name="create_mentor_profile")
]