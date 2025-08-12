import os
from datetime import timedelta, date, datetime

import django
from django.db.models.aggregates import Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Song, Artist, Product, Review, Driver, DrivingLicense, Owner, Car, \
    Registration


# Create queries within functions


def show_all_authors_with_their_books():
    authors = Author.objects.all().order_by("id")
    authors_with_books = []

    for author in authors:
        books = Book.objects.filter(author=author)

        if not books:
            continue

        titles = ', '.join(b.title for b in books)
        authors_with_books.append(
            f"{author.name} has written - {titles}!"
        )

    return "\n".join(authors_with_books)

    # for author in Author.objects.all().order_by('id'):
    #     if author.books:
    #         return '\n'.join(f"{author} has written - {b.title}!" for b in author.books.all())
    #     else:
    #         continue


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


##############################################################


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


################################################################


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    return product.reviews.aggregate(Avg('rating'))['rating__avg']


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


#################################################################


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    result = []
    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)
        result.append(f'License with number: {license.license_number} expires on {expiration_date}!')
    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date):
    expired_licenses = DrivingLicense.objects.filter(issue_date__lte=due_date - timedelta(days=365))
    return [license.driver for license in expired_licenses]

    ################################################


def register_car_by_owner(owner: Owner) -> str:
    car = Car.objects.filter(registration__isnull=True).first()
    registration = Registration.objects.filter(car__isnull=True).first()

    car.owner = owner
    car.registration = registration

    car.save()

    registration.registration_date = datetime.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."
