import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import RealEstateListing, VideoGame, BillingInfo, Invoice, Project, Technology, Programmer, \
    Exercise
from main_app.managers import VideoGameManager








