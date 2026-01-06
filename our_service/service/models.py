from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Short description for the home page")
    detailed_description = models.TextField(blank=True, help_text="Full description for the details page")
    technologies = models.TextField(blank=True, help_text="Comma-separated list of technologies (e.g., Python, Django, React)")
    icon = models.CharField(max_length=50, help_text="FontAwesome class or similar", default="fa-code")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        if self.technologies:
            return [x.strip() for x in self.technologies.split(',')]
        return []

class Project(models.Model):
    title = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    client = models.CharField(max_length=100, blank=True)
    live_url = models.URLField(blank=True, help_text="Link to the live project")
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    quote = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    features = models.TextField(help_text="Comma-separated list of features")
    is_popular = models.BooleanField(default=False)
    button_text = models.CharField(max_length=50, default="Get Started")
    
    def get_features_list(self):
        if self.features:
            return [x.strip() for x in self.features.split(',')]
        return []

    def __str__(self):
        return self.name

class ClientLogo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/')
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class OfficeInfo(models.Model):
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    map_embed_url = models.TextField(blank=True, help_text="Google Maps Embed Iframe Src")
    
    class Meta:
        verbose_name_plural = "Office Information"

    def __str__(self):
        return "Office Details"

class CompanyProfile(models.Model):
    title = models.CharField(max_length=200, default="About Us")
    story = models.TextField(help_text="Our Story")
    mission = models.TextField(help_text="Our Mission")
    vision = models.TextField(help_text="Our Vision")
    about_image = models.ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Company Profile"
        
    def __str__(self):
        return "Company Profile"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class ChatMessage(models.Model):
    sender_name = models.CharField(max_length=100, default="Anonymous") 
    message = models.TextField()
    is_admin = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"{self.sender_name}: {self.message[:20]}"
