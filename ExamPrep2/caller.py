import os
from itertools import product

import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Profile, Order, Product


# Create queries within functions
#
#
# def populate_db():
#     profile_1 = Profile.objects.create(
#         full_name="Adam Smith",
#         email="adam.smith@example.com",
#         phone_number="123456789",
#         address="123 Main St. Springfield",
#         is_active=True,
#     )
#     profile_2 = Profile.objects.create(
#         full_name="Susan James",
#         email="susan.james@example.com",
#         phone_number="987654321",
#         address="456 Elm St, Metropolis",
#         is_active=True,
#     )
#
#     product_1 = Product.objects.create(
#         name="Desk M",
#         description="A medium-sized office desk",
#         price=150.00,
#         in_stock=10,
#         is_available=True,
#     )
#
#     product_2 = Product.objects.create(
#         name="Display DL",
#         description="A 24-inch HD display",
#         price=200.00,
#         in_stock=5,
#         is_available=True,
#     )
#
#     product_3 = Product.objects.create(
#         name="Printer Br PM",
#         description="A high-speed printer",
#         price=300.00,
#         in_stock=3,
#         is_available=True,
#     )
#
#     order_1 = Order.objects.create(
#         profile=profile_1,
#         total_price=350,
#     )
#
#     order_2 = Order.objects.create(
#         profile=profile_1,
#         total_price=300,
#
#     )
#
#     order_3 = Order.objects.create(
#         profile=profile_1,
#         total_price=300,
#
#     )

