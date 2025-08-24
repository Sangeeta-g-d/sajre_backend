from django.urls import path
from . import views

urlpatterns = [
    path('a_index/',views.a_index,name="a_index"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('vendor_list/',views.vendor_list,name="vendor_list"),
    path('vendor_details/<int:vendor_id>/',views.vendor_details,name="vendor_details"),
    path('mentors/',views.mentors,name="mentors"),
    path('view_mentor_details/<int:mentor_id>/',views.view_mentor_details,name="view_mentor_details"),
    path('participants_list/',views.participants_list,name="participants_list"),


    # competition
    path('competition_category_list/',views.competition_category_list,name="competition_category_list"),
    path('add_competition_category/',views.add_competition_category,name="add_competition_category"),
    path("delete_category/<int:pk>/", views.delete_competition_category, name="delete_competition_category"),
    path("edit_category/<int:pk>/", views.edit_competition_category, name="edit_competition_category"),
    path("categories/<int:category_id>/levels/", views.get_category_levels, name="get_category_levels"),

    # level
    path('add_level/<int:category_id>/',views.add_level,name="add_level"),
    path('delete_level/<int:level_id>/',views.delete_level,name="delete_level"),
    path('level_info/<int:level_id>/', views.level_info, name='level_info'),
    path("add-round/", views.add_round, name="add_round"),
    path("add-or-update-schedule/", views.add_or_update_schedule, name="add_or_update_schedule"),
    # path("update-last-date/", views.update_last_date, name="update_last_date"),
    path("edit_level/<int:level_id>/", views.edit_level, name="edit_level"),

    # FAQ
    path('view_faq/',views.view_faq,name="view_faq"),
    path("add_faq/", views.add_faq, name="add_faq"),
    path("faqs/<str:role>/", views.view_faqs_by_role, name="view_faqs_by_role"),   
    path("delete_faq/<int:faq_id>/", views.delete_faq, name="delete_faq"),
    path('enrolled_list/<int:level_id>/',views.enrolled_list,name="enrolled_list"),


]