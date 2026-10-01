import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def max_year() -> int:
    return datetime.date.today().year


class Reader(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        default="avatars/default.jpg"
    )


class Book(models.Model):
    title = models.CharField(max_length=255)
    pages = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    year_published = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=max_year,
                message="Are you sure that your book is from future?)"
            )
        ]
    )
    publisher = models.CharField(max_length=255)
    cover_image = models.ImageField(
        upload_to="book_covers/",
        null=True,
        blank=True,
        default="book_covers/default.jpg"
    )
    genres = models.ManyToManyField(
        to="Genre",
        related_name="books"
    )
    authors = models.ManyToManyField(
        to="Author",
        related_name="books"
    )


class Genre(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    pseudonym = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(
        upload_to="author_photos/",
        null=True,
        blank=True,
        default="author_photos/default.jpg"
    )
    country = models.CharField(max_length=255, blank=True, null=True)

    @property
    def is_alive(self) -> bool:
        return self.death_date is None


class Shelf(models.Model):
    name = models.CharField(max_length=255)
    reader = models.ForeignKey(
        to="Reader",
        on_delete=models.CASCADE
    )
    books = models.ManyToManyField(
        to="Book",
        related_name="shelves"
    )


class ReaderBook(models.Model):
    class StatusName(models.TextChoices):
        WANT_TO_READ = "want_to_read", "Want to read"
        CURRENTLY_READING = "currently_reading", "Currently reading"
        READ = "read", "Read"
        DID_NOT_FINISH = "did_not_finish", "Did not finish"

    reader = models.ForeignKey(
        to="Reader",
        on_delete=models.CASCADE,
        related_name="reader_books"
    )
    book = models.ForeignKey(
        to="Book",
        on_delete=models.CASCADE,
        related_name="reader_books"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusName.choices,
        blank=True, null=True
    )
    rating = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    review = models.TextField(blank=True, null=True)
    started_at = models.DateField(blank=True, null=True)
    finished_at = models.DateField(blank=True, null=True)
