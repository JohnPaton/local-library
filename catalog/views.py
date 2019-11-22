from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre

# Create your views here.
def index(request):
    """Home page"""

    # Generate counts
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Available books (status "a")
    num_instances_available = BookInstance.objects.filter(
        status__exact="a"
    ).count()

    num_authors = Author.objects.count()

    return render(request, "index.html", context=locals())
