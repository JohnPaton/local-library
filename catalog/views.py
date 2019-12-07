from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Book, Author, BookInstance, Genre

# Create your views here.

# index is a function-based view
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

    # Number of visits by this browser (from sessions)
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    return render(request, "index.html", context=locals())


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    queryset = Book.objects.order_by("title", "author")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Create any data and add it to the context
        context["my_extra_context_var"] = "This is just some data"
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    queryset = Author.objects.order_by(
        "last_name", "first_name", "date_of_birth"
    )


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """List of books on loan to the current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )
