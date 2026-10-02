from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest

from digital_library.models import Reader, Book, Genre, Author, ReaderBook, Shelf


@admin.register(Reader)
class ReaderAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("birth_date", "avatar")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("birth_date", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "avatar"
                )
            }
        ),
    )
    ordering = ("username", )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pages",
        "year_published",
        "publisher",
        "authors_list",
        "genres_list",
        "cover_image",
    )
    list_filter = (
        "genres__name",
        "authors",
    )
    ordering = ("title", "authors")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related(
            "authors",
            "genres"
        )

    @admin.display(description="Authors")
    def authors_list(self, obj):
        return ", ".join(str(author) for author in obj.authors.all())

    @admin.display(description="Genres")
    def genres_list(self, obj):
        return ", ".join(genre.name for genre in obj.genres.all())


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )


class IsAliveFilter(admin.SimpleListFilter):
    title = "is alive"
    parameter_name = "is_alive"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Alive"),
            ("no", "Deceased"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(death_date__isnull=True)
        if self.value() == "no":
            return queryset.filter(death_date__isnull=False)
        return queryset


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "pseudonym",
        "is_alive",
        "country",
        "photo"
    )
    list_filter = (
        IsAliveFilter,
        "country",
    )
    search_fields = (
        "first_name",
        "last_name",
        "pseudonym"
    )


@admin.register(ReaderBook)
class ReaderBookAdmin(admin.ModelAdmin):
    list_display = ("reader", "book", "status", "rating")
    list_filter = ("status",)
    search_fields = ("reader__username", "book__title")


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ("name", "reader")
    search_fields = ("name", "reader__username")