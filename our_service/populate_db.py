import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'our_service.settings')
django.setup()

from service.models import Service, TeamMember, OfficeInfo

def populate():
    # Services
    services = [
        {
            'title': 'Custom Web Development',
            'description': 'High-performance websites tailored to your exact business needs using the latest technologies like Django, React, and Next.js.',
            'icon': 'fa-code'
        },
        {
            'title': 'Mobile App Solutions',
            'description': 'Native and Cross-platform mobile applications that provide seamless user experiences on iOS and Android.',
            'icon': 'fa-mobile-alt'
        },
        {
            'title': 'Digital Marketing',
            'description': 'Data-driven marketing strategies to grow your audience and convert visitors into loyal customers.',
            'icon': 'fa-bullhorn'
        },
         {
            'title': 'UI/UX Design',
            'description': 'We design intuitive and beautiful interfaces that ensure your products are a joy to use.',
            'icon': 'fa-paint-brush'
        }
    ]

    for s in services:
        Service.objects.get_or_create(title=s['title'], defaults=s)
    
    print("Services created.")

    # Team
    team = [
        {
            'name': 'Rahim Ahmed',
            'role': 'Lead Developer',
            'bio': 'Full Stack expert with 5 years experience.'
        },
        {
            'name': 'Karim Islam',
            'role': 'UI/UX Designer',
            'bio': 'Creative designer with a passion for user-centric design.'
        },
        {
            'name': 'Fatima Begum',
            'role': 'Project Manager',
            'bio': 'Organized and detail-oriented manager ensuring timely delivery.'
        }
    ]

    for t in team:
        TeamMember.objects.get_or_create(name=t['name'], defaults=t)
        
    print("Team created.")

    # Office
    if not OfficeInfo.objects.exists():
        OfficeInfo.objects.create(
            address='Level 4, Tech Tower, Gulshan-1, Dhaka',
            email='info@ourtechagency.com',
            phone='+880 1711 000000'
        )
    print("Office info created.")

if __name__ == '__main__':
    populate()
