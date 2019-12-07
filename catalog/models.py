import uuid
from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


class AutoTiming(models.Model):
    """An abstract model for saving timing information"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(AutoTiming):
    """Represents a book genre."""

    name = models.CharField(
        max_length=200, help_text="Enter a book genre (e.g. Science Fiction)"
    )

    def __str__(self):
        return self.name


class Language(AutoTiming):
    """A book's language"""

    name = models.CharField(
        max_length=100, help_text="Enter a language (e.g. English)"
    )

    def __str__(self):
        return f"{self.name}"


class Book(AutoTiming):
    """Represents a book (in general, not a specific copy)"""

    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
    )
    isbn = models.CharField(
        "ISBN", max_length=13, help_text="13 Character ISBN"
    )
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book"
    )
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (
            f"{self.author.last_name}, {self.author.first_name} - {self.title}"
        )

    def get_absolute_url(self):
        """The url for the detail view of this book"""
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """Display the top 3 genres in string form"""
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


class BookInstance(AutoTiming):
    """A specific copy of a book (that can be borrowed from the library)"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this book copy across the whole library",
    )
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.id} ({self.book.title})"


class Author(AutoTiming):
    """An author of books"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """The url for the detail view of this author"""
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
