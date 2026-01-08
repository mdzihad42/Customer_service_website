from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('projects/', views.project_list, name='project_list'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('chat/get/', views.chat_get_messages, name='chat_get'),
    path('chat/send/', views.chat_send_message, name='chat_send'),
    path('chat/read/', views.chat_mark_read, name='chat_mark_read'),
    path('chat/notifications/', views.chat_unread_count, name='chat_notifications'),
    
    # PWA
    path('manifest.json', views.manifest_view, name='manifest'),
    path('service-worker.js', views.service_worker_view, name='service_worker'),

    # Dashboard URLs
    path('custom-admin/', views.dashboard_home, name='dashboard_home'),
    
    path('custom-admin/services/', views.dashboard_services, name='dashboard_services'),
    path('custom-admin/services/new/', views.dashboard_service_edit, name='dashboard_service_create'),
    path('custom-admin/services/edit/<int:pk>/', views.dashboard_service_edit, name='dashboard_service_edit'),
    path('custom-admin/services/delete/<int:pk>/', views.dashboard_service_delete, name='dashboard_service_delete'),

    path('custom-admin/projects/', views.dashboard_projects, name='dashboard_projects'),
    path('custom-admin/projects/new/', views.dashboard_project_edit, name='dashboard_project_create'),
    path('custom-admin/projects/edit/<int:pk>/', views.dashboard_project_edit, name='dashboard_project_edit'),
    path('custom-admin/projects/delete/<int:pk>/', views.dashboard_project_delete, name='dashboard_project_delete'),

    path('custom-admin/blog/', views.dashboard_blogs, name='dashboard_blogs'),
    path('custom-admin/blog/new/', views.dashboard_blog_edit, name='dashboard_blog_create'),
    path('custom-admin/blog/edit/<int:pk>/', views.dashboard_blog_edit, name='dashboard_blog_edit'),
    path('custom-admin/blog/delete/<int:pk>/', views.dashboard_blog_delete, name='dashboard_blog_delete'),

    path('custom-admin/team/', views.dashboard_team, name='dashboard_team'),
    path('custom-admin/team/new/', views.dashboard_team_edit, name='dashboard_team_create'),
    path('custom-admin/team/edit/<int:pk>/', views.dashboard_team_edit, name='dashboard_team_edit'),
    path('custom-admin/team/delete/<int:pk>/', views.dashboard_team_delete, name='dashboard_team_delete'),

    path('custom-admin/contacts/', views.dashboard_contacts, name='dashboard_contacts'),
    path('custom-admin/contacts/delete/<int:pk>/', views.dashboard_contact_delete, name='dashboard_contact_delete'),

    path('custom-admin/office/', views.dashboard_office, name='dashboard_office'),
    path('custom-admin/profile/', views.dashboard_profile, name='dashboard_profile'),
    path('custom-admin/chat/', views.dashboard_chat, name='dashboard_chat'),
    path('custom-admin/chat/delete/<str:session_id>/', views.dashboard_chat_delete, name='dashboard_chat_delete'),

    path('custom-admin/testimonials/', views.dashboard_testimonials, name='dashboard_testimonials'),
    path('custom-admin/testimonials/new/', views.dashboard_testimonial_edit, name='dashboard_testimonial_create'),
    path('custom-admin/testimonials/edit/<int:pk>/', views.dashboard_testimonial_edit, name='dashboard_testimonial_edit'),
    path('custom-admin/testimonials/delete/<int:pk>/', views.dashboard_testimonial_delete, name='dashboard_testimonial_delete'),

    path('custom-admin/tech/', views.dashboard_tech_list, name='dashboard_tech_list'),
    path('custom-admin/tech/new/', views.dashboard_tech_edit, name='dashboard_tech_create'),
    path('custom-admin/tech/edit/<int:pk>/', views.dashboard_tech_edit, name='dashboard_tech_edit'),
    path('custom-admin/tech/delete/<int:pk>/', views.dashboard_tech_delete, name='dashboard_tech_delete'),

    path('custom-admin/pricing/', views.dashboard_pricing, name='dashboard_pricing'),
    path('custom-admin/pricing/new/', views.dashboard_pricing_edit, name='dashboard_pricing_create'),
    path('custom-admin/pricing/edit/<int:pk>/', views.dashboard_pricing_edit, name='dashboard_pricing_edit'),
    path('custom-admin/pricing/delete/<int:pk>/', views.dashboard_pricing_delete, name='dashboard_pricing_delete'),

    path('custom-admin/clients/', views.dashboard_clients, name='dashboard_clients'),
    path('custom-admin/clients/new/', views.dashboard_client_edit, name='dashboard_client_create'),
    path('custom-admin/clients/edit/<int:pk>/', views.dashboard_client_edit, name='dashboard_client_edit'),
    path('custom-admin/clients/delete/<int:pk>/', views.dashboard_client_delete, name='dashboard_client_delete'),
    
    path('custom-admin/faqs/', views.dashboard_faqs, name='dashboard_faqs'),
    path('custom-admin/faqs/new/', views.dashboard_faq_edit, name='dashboard_faq_create'),
    path('custom-admin/faqs/edit/<int:pk>/', views.dashboard_faq_edit, name='dashboard_faq_edit'),
    path('custom-admin/faqs/delete/<int:pk>/', views.dashboard_faq_delete, name='dashboard_faq_delete'),
]
