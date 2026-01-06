from django.contrib import admin
from .models import Service, TeamMember, OfficeInfo, ContactMessage, ChatMessage, Project, BlogPost, CompanyProfile, Testimonial, FAQ, PricingPlan, ClientLogo

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')

@admin.register(OfficeInfo)
class OfficeInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'email', 'phone')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'message', 'is_admin', 'created_at', 'session_id')
    list_filter = ('is_admin', 'created_at')
    search_fields = ('message', 'sender_name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'client', 'completed_date')
    list_filter = ('service', 'completed_date')
    search_fields = ('title', 'description', 'client')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'created_at')
    search_fields = ('client_name', 'quote', 'company')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    search_fields = ('question', 'answer')

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'features')

@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url')
    search_fields = ('name',)
