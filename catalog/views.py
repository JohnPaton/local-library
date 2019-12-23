import datetime


from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm

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


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """List of all books on loan in the whole library"""

    model = BookInstance
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/bookinstance_list_borrowed_librarian.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by(
            "due_back"
        )


@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    """Renew a specific BookInstance as a librarian"""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Bind a form instance
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # use data from form.cleaned_data and NOT request.POST
            # It's validated and also cast to Python types
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()

            return HttpResponseRedirect(reverse("borrowed"))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(
            weeks=3
        )
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {"form": form, "book_instance": book_instance}

    return render(request, "catalog/book_renew_librarian.html", context)


class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"
    # initial = {"date_of_death": "05/01/2018"}  # just for show


class AuthorUpdate(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("authors")


class BookCreate(CreateView):
    model = Book
    fields = "__all__"


class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("books")
