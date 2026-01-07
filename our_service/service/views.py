from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import dns.resolver

from .models import Service, TeamMember, OfficeInfo, ContactMessage, ChatMessage, Project, BlogPost, CompanyProfile, Testimonial, FAQ, PricingPlan, ClientLogo, TechStack
from .forms import ServiceForm, TeamMemberForm, OfficeInfoForm, ProjectForm, BlogPostForm, CompanyProfileForm, TestimonialForm, TechStackForm, PricingPlanForm, ClientLogoForm
from django.db.models import Count, Max
import uuid

def home(request):
    services = Service.objects.all()
    team = TeamMember.objects.all()
    office = OfficeInfo.objects.first()
    recent_projects = Project.objects.order_by('-completed_date')[:3]
    recent_blogs = BlogPost.objects.order_by('-created_at')[:3]
    
    if 'chat_session_id' not in request.session:
        request.session['chat_session_id'] = str(uuid.uuid4())
    
    testimonials = Testimonial.objects.order_by('-created_at')[:5]
    faqs = FAQ.objects.all()
    pricing_plans = PricingPlan.objects.all()
    pricing_plans = PricingPlan.objects.all()
    clients = ClientLogo.objects.all()
    tech_stacks = TechStack.objects.all()
    
    context = {
        'services': services,
        'team': team,
        'office': office,
        'recent_projects': recent_projects,
        'recent_blogs': recent_blogs,
        'testimonials': testimonials,
        'faqs': faqs,
        'pricing_plans': pricing_plans,
        'clients': clients,
        'tech_stacks': tech_stacks
    }
    return render(request, 'home.html', context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    projects = service.projects.all()
    return render(request, 'service_detail.html', {'service': service, 'projects': projects})

def project_list(request):
    projects = Project.objects.all().order_by('-completed_date')
    return render(request, 'projects.html', {'projects': projects})

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    recent_posts = BlogPost.objects.exclude(pk=pk).order_by('-created_at')[:3]
    return render(request, 'blog_detail.html', {'post': post, 'recent_posts': recent_posts})

def about_us(request):
    profile = CompanyProfile.objects.first()
    team = TeamMember.objects.all()
    office = OfficeInfo.objects.first()
    return render(request, 'about.html', {'profile': profile, 'team': team, 'office': office})

def validate_email_address(email):
    try:
        # 1. Syntax Check
        validate_email(email)
        
        # 2. DNS Check (MX Record)
        domain = email.split('@')[1]
        try:
            dns.resolver.resolve(domain, 'MX')
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
             return False
        except Exception:
             return False # Fail safe
             
        return True
    except ValidationError:
        return False

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if not validate_email_address(email):
            messages.error(request, "Invalid email address! Please provide a real email.")
            return redirect('home')

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, "Message sent successfully!")
        return redirect('home')
    return redirect('home')

def chat_get_messages(request):
    # If admin is checking a specific session
    target_session = request.GET.get('session_id')
    if request.user.is_staff and target_session:
        session_id = target_session
    else:
        session_id = request.session.get('chat_session_id')

    if not session_id:
         return JsonResponse([], safe=False)

    messages = ChatMessage.objects.filter(session_id=session_id).order_by('created_at').values('sender_name', 'message', 'is_admin', 'created_at')
    return JsonResponse(list(messages), safe=False)

@csrf_exempt
def chat_send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        
        # Determine if Admin or Guest
        if request.user.is_staff and request.POST.get('is_admin') == 'true':
             # Admin sending to a specific session
             session_id = request.POST.get('session_id')
             sender_name = "Support Team"
             is_admin = True
        else:
             # Guest sending to their own session
             session_id = request.session.get('chat_session_id')
             sender_name = "Guest"
             is_admin = False

        if message and session_id:
            ChatMessage.objects.create(
                sender_name=sender_name,
                message=message,
                session_id=session_id,
                is_admin=is_admin
            )
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def chat_mark_read(request):
    """Marks all appropriate messages as read for the current session."""
    if request.method == 'POST':
        session_id = request.session.get('chat_session_id')
        if session_id:
            # If guest is calling, mark Admin's messages as read
            if not request.user.is_staff:
                ChatMessage.objects.filter(session_id=session_id, is_admin=True, is_read=False).update(is_read=True)
            # If admin is calling, logic would be different (marking User's messages), but usually managed differently
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def chat_unread_count(request):
    """Returns number of unread messages for the guest."""
    session_id = request.session.get('chat_session_id')
    count = 0
    if session_id:
        # Check for unread messages FROM admin
        count = ChatMessage.objects.filter(session_id=session_id, is_admin=True, is_read=False).count()
    return JsonResponse({'unread_count': count})

# --- Dashboard Views ---

@staff_member_required
def dashboard_home(request):
    total_services = Service.objects.count()
    total_team = TeamMember.objects.count()
    total_messages = ContactMessage.objects.count()
    total_projects = Project.objects.count()
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    
    context = {
        'total_services': total_services,
        'total_team': total_team,
        'total_messages': total_messages,
        'total_projects': total_projects,
        'recent_messages': recent_messages
    }
    return render(request, 'dashboard/home.html', context)

@staff_member_required
def dashboard_services(request):
    services = Service.objects.all()
    return render(request, 'dashboard/service_list.html', {'services': services})

@staff_member_required
def dashboard_service_edit(request, pk=None):
    if pk:
        service = get_object_or_404(Service, pk=pk)
    else:
        service = None
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('dashboard_services')
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Service'})

@staff_member_required
def dashboard_service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('dashboard_services')

@staff_member_required
def dashboard_projects(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})

@staff_member_required
def dashboard_project_edit(request, pk=None):
    if pk:
        project = get_object_or_404(Project, pk=pk)
    else:
        project = None
        
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard_projects')
    else:
        form = ProjectForm(instance=project)
        
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Project'})

@staff_member_required
def dashboard_project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('dashboard_projects')

@staff_member_required
def dashboard_blogs(request):
    posts = BlogPost.objects.all()
    return render(request, 'dashboard/blog_list.html', {'posts': posts})

@staff_member_required
def dashboard_blog_edit(request, pk=None):
    if pk:
        post = get_object_or_404(BlogPost, pk=pk)
    else:
        post = None
        
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            blog = form.save(commit=False)
            if not pk:
                blog.author = request.user
            blog.save()
            return redirect('dashboard_blogs')
    else:
        form = BlogPostForm(instance=post)
        
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Blog Post'})

@staff_member_required
def dashboard_blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('dashboard_blogs')

@staff_member_required
def dashboard_team(request):
    team = TeamMember.objects.all()
    return render(request, 'dashboard/team_list.html', {'team': team})

@staff_member_required
def dashboard_team_edit(request, pk=None):
    if pk:
        member = get_object_or_404(TeamMember, pk=pk)
    else:
        member = None

    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('dashboard_team')
    else:
        form = TeamMemberForm(instance=member)

    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Team Member'})

@staff_member_required
def dashboard_team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()
    return redirect('dashboard_team')

@staff_member_required
def dashboard_contacts(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'dashboard/contact_list.html', {'messages_list': messages_list})

@staff_member_required
def dashboard_contact_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    return redirect('dashboard_contacts')

@staff_member_required
def dashboard_office(request):
    office = OfficeInfo.objects.first()
    if request.method == 'POST':
        form = OfficeInfoForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    else:
        form = OfficeInfoForm(instance=office)
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Office Info'})

@staff_member_required
def dashboard_profile(request):
    profile = CompanyProfile.objects.first()
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Company Profile (About Us)'})

@staff_member_required
def dashboard_chat(request):
    # Get all unique sessions with their last message
    sessions = ChatMessage.objects.values('session_id').annotate(
        last_msg_time=Max('created_at'),
        msg_count=Count('id')
    ).order_by('-last_msg_time')
    
    # Decorate sessions with last message preview
    active_sessions = []
    for s in sessions:
        last_msg = ChatMessage.objects.filter(session_id=s['session_id']).latest('created_at')
        active_sessions.append({
            'session_id': s['session_id'],
            'last_message': last_msg.message,
            'time': last_msg.created_at,
            'is_admin': last_msg.is_admin
        })

    return render(request, 'dashboard/chat.html', {'sessions': active_sessions})

@staff_member_required
def dashboard_chat_delete(request, session_id):
    ChatMessage.objects.filter(session_id=session_id).delete()
    return redirect('dashboard_chat')

@staff_member_required
def dashboard_testimonials(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'dashboard/testimonial_list.html', {'testimonials': testimonials})

@staff_member_required
def dashboard_testimonial_edit(request, pk=None):
    if pk:
        testimonial = get_object_or_404(Testimonial, pk=pk)
    else:
        testimonial = None

    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            return redirect('dashboard_testimonials')
    else:
        form = TestimonialForm(instance=testimonial)

    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Testimonial'})

@staff_member_required
def dashboard_testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    return redirect('dashboard_testimonials')

@staff_member_required
def dashboard_tech_list(request):
    techs = TechStack.objects.all()
    return render(request, 'dashboard/tech_list.html', {'techs': techs})

@staff_member_required
def dashboard_tech_edit(request, pk=None):
    if pk:
        tech = get_object_or_404(TechStack, pk=pk)
    else:
        tech = None

    if request.method == 'POST':
        form = TechStackForm(request.POST, request.FILES, instance=tech)
        if form.is_valid():
            form.save()
            return redirect('dashboard_tech_list')
    else:
        form = TechStackForm(instance=tech)

    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Technology'})

@staff_member_required
def dashboard_tech_delete(request, pk):
    tech = get_object_or_404(TechStack, pk=pk)
    tech.delete()
    return redirect('dashboard_tech_list')

@staff_member_required
def dashboard_pricing(request):
    plans = PricingPlan.objects.all()
    return render(request, 'dashboard/pricing_list.html', {'plans': plans})

@staff_member_required
def dashboard_pricing_edit(request, pk=None):
    if pk:
        plan = get_object_or_404(PricingPlan, pk=pk)
    else:
        plan = None

    if request.method == 'POST':
        form = PricingPlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('dashboard_pricing')
    else:
        form = PricingPlanForm(instance=plan)

    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Pricing Plan'})

@staff_member_required
def dashboard_pricing_delete(request, pk):
    plan = get_object_or_404(PricingPlan, pk=pk)
    plan.delete()
    return redirect('dashboard_pricing')

@staff_member_required
def dashboard_clients(request):
    clients = ClientLogo.objects.all()
    return render(request, 'dashboard/client_list.html', {'clients': clients})

@staff_member_required
def dashboard_client_edit(request, pk=None):
    if pk:
        client = get_object_or_404(ClientLogo, pk=pk)
    else:
        client = None

    if request.method == 'POST':
        form = ClientLogoForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('dashboard_clients')
    else:
        form = ClientLogoForm(instance=client)

    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Client Logo'})

@staff_member_required
def dashboard_client_delete(request, pk):
    client = get_object_or_404(ClientLogo, pk=pk)
    client.delete()
    return redirect('dashboard_clients')
