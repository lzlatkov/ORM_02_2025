import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book


# Create queries within functions


def get_publishers(search_string=None):
    if search_string is None:
        return "No search criteria."
    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) | Q(country__icontains=search_string)).order_by('-rating', 'name')
    if not publishers:
        return "No publishers found."
    return '\n'.join(
        f"Publisher: {p.name}, country: {'Unknown' if p.country == 'TBC' else p.country}, rating: {p.rating:.1f}" for p
        in publishers
    )


def get_top_publisher():
    top_publisher = Publisher.objects.get_publishers_by_books_count().first()
    if not top_publisher:
        return "No publishers found."
    return f"Top Publisher: {top_publisher.name} with {top_publisher.books_count} books."


def get_top_main_author():
    best_author = Author.objects.annotate(books_count=Count('main_author_books'),
                                          books_average_rating=Avg('main_author_books__rating')
                                          ).order_by('-books_count', 'name').first()

    if not best_author or best_author.books_count == 0:
        return "No results."

    books = Book.objects.filter(main_author=best_author).order_by('title').values_list('title', flat=True)
    avg_rating = best_author.books_average_rating

    return f"Top Author: {best_author.name}, own book titles: {', '.join(books)}, books average rating: {avg_rating:.1f}"


def get_authors_by_books_count():
    all_authors = Author.objects.annotate(books_count=Count('main_author_books') + Count('coauthor_books')
                                          ).order_by('-books_count', 'name')[:3]

    if not all_authors or not Book.objects.exists():
        return "No results."
    return '\n'.join(f"{a.name} authored {a.books_count} books." for a in all_authors)


def get_top_bestseller():
    best_bestseller = Book.objects.filter(is_bestseller=True).order_by('-rating', 'title').first()
    if not best_bestseller:
        return "No results."
    all_co_authors = best_bestseller.co_authors.all().order_by('name').values_list('name', flat=True)
    print_helper = ', '.join(all_co_authors) if all_co_authors else "N/A"
    return (f"Top bestseller: {best_bestseller.title}, rating: {best_bestseller.rating:.1f}. Main author: "
            f"{best_bestseller.main_author.name}. Co-authors: {print_helper}.")


def increase_price():
    books_to_update = Book.objects.filter(publication_date__year=2025, rating__gte=4.0)
    updated_books = books_to_update.update(price=F('price') * 1.2)
    if not updated_books:
        return "No changes in price."
    return f"Prices increased for {updated_books} books."
