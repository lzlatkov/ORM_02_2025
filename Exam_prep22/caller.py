import os
import django
from django.db.models import Q, Count, Sum, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


# Create queries within functions


def get_profiles(search_string=None):
    if search_string is None:
        return ''

    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(
        phone_number__icontains=search_string)
    profiles = Profile.objects.filter(query).annotate(orders_count=Count('order')).order_by('full_name')

    return '\n'.join(f"Profile: {p.full_name}, email: {p.email}, "
                     f"phone number: {p.phone_number}, orders: {p.orders_count}" for p in profiles)


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()
    return '\n'.join(f"Profile: {p.full_name}, orders: {p.orders_count}" for p in loyal_profiles)


def get_last_sold_products():
    last_order = Order.objects.order_by('products').last()
    if not last_order:
        return ''
    products = last_order.products.order_by('name').values_list('name', flat=True)
    return f"Last sold products: {', '.join(products)}"


def get_top_products():
    top_products = Product.objects.annotate(orders_count=Count('order')).filter(
        orders_count__gt=0,).order_by('-orders_count', 'name')[:5]
    if not top_products:
        return ''
    result = ["Top products:"]
    for product in top_products:
        result.append(f"{product.name}, sold {product.orders_count} times")

    return "\n".join(result)


def apply_discounts():
    to_update = (Order.objects.annotate(product_count=Count('products')).
                 filter(product_count__gt=2, is_completed=False).update(total_price=F('total_price') * 0.9))

    return f"Discount applied to {to_update} orders."


def complete_order():
    first_not_completed_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()
    if not first_not_completed_order:
        return ''

    products = first_not_completed_order.products.all()
    for product in products:
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    first_not_completed_order.is_completed = True
    first_not_completed_order.save()
    return f"Order has been completed!"

