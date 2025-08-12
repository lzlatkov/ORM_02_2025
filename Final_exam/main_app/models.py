from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import PublisherManager


# Create your models here.


# class Publisher(models.Model):
#     name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
#     established_date = models.DateField(default='1800-01-01')
#     country = models.CharField(max_length=40, default='TBC')
#     rating = models.FloatField(validators=[
#         MinValueValidator(0.0),
#         MaxValueValidator(5.0),
#     ], default=0.0)
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
#     birth_date = models.DateField(blank=True, null=True)
#     country = models.CharField(max_length=40, default='TBC')
#     is_active = models.BooleanField(default=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class Book(models.Model):
#     class GenreChoices(models.TextChoices):
#         Fiction = 'Fiction'
#         NonFiction = 'Non-Fiction'
#         Other = 'Other'
#     title = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
#     publication_date = models.DateField(blank=True, null=True)
#     summary = models.TextField(blank=True, null=True)
#     genre = models.CharField(max_length=11, choices=GenreChoices, default=GenreChoices.Other)
#     price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(9999.99)], default=0.01)
#     rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0)
#     is_bestseller = models.BooleanField(default=False)
#     updated_at = models.DateTimeField(auto_now=True)
#     publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
#     main_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='main_author_books')
#     co_authors = models.ManyToManyField(Author, related_name='co_authors_books')

class Publisher(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
    )
    established_date = models.DateField(default='1800-01-01')
    country = models.CharField(
        max_length=40,
        default='TBC',
    )
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    objects = PublisherManager()


class Author(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
    )
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(
        max_length=40,
        default='TBC',
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    OTHER = 'Other'

    GENRE_CHOICES = [
        (FICTION, 'Fiction'),
        (NON_FICTION, 'Non-Fiction'),
        (OTHER, 'Other'),
    ]

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)],
    )
    publication_date = models.DateField()
    summary = models.TextField(null=True, blank=True)
    genre = models.CharField(
        max_length=11,
        choices=GENRE_CHOICES,
        default=OTHER,
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.01,
        validators=[MinValueValidator(0.01), MaxValueValidator(9999.99)],
    )
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    is_bestseller = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
    )
    main_author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='main_author_books',
    )
    co_authors = models.ManyToManyField(
        Author,
        related_name='coauthor_books',
        blank=True,
    )