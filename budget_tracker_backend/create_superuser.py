import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
    User.objects.create_superuser(
        os.environ['DJANGO_SUPERUSER_USERNAME'],
        os.environ['DJANGO_SUPERUSER_EMAIL'],
        os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists")