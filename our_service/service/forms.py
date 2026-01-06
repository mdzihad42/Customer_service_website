from django import forms
from .models import Service, TeamMember, OfficeInfo, Project, BlogPost, CompanyProfile, Testimonial

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'
        widgets = {
            'quote': forms.Textarea(attrs={'rows': 4}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class OfficeInfoForm(forms.ModelForm):
    class Meta:
        model = OfficeInfo
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'map_embed_url': forms.Textarea(attrs={'rows': 3}),
        }

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = '__all__'
        widgets = {
            'story': forms.Textarea(attrs={'rows': 5}),
            'mission': forms.Textarea(attrs={'rows': 3}),
            'vision': forms.Textarea(attrs={'rows': 3}),
        }
