# Server live!
https://digital-library-4wjf.onrender.com/

# Digital Library

A book-tracking website built with Django. Readers can browse books, rate and
review what they've read, organize their personal library into shelves, and
discover new titles through the highest-rated picks on the home page.

Built as a portfolio project for Mate Academy.

## Features

- Browse books, authors, and genres with search and pagination
- Rate books (1–10) and leave reviews
- Organize books into personal shelves (default shelves are created
  automatically on registration; custom shelves can be added)
- Average rating shown with a star-rating display, plus recent reviews
  on each book's page
- Author pages show a black-and-white photo for authors who have passed away
- Any logged-in reader can add new books and authors; only staff can edit or
  delete existing records
- User registration and profile editing
- Django admin configured for all models, with search and filtering
  (including a custom "is alive" filter for authors)

## Tech stack

- Python, Django
- SQLite (default)
- Bootstrap 4
- Pillow (for image fields)

## Project structure

- `core/` — Django project settings
- `digital_library/` — main app: models, views, forms, templates, static files

## Screenshots

**Home page** — a grid of the highest-rated books, pulled randomly from the
top 20 by average rating.
![Home page](docs/screenshots/home.png)

**Book list** — searchable, paginated table with cover, genres, authors,
year, and a star rating for each book.
![Book list](docs/screenshots/book_list.png)

**Author list** — searchable table of authors with photo, country, and the
books they've written.
![Author list](docs/screenshots/author_list.png)

**Genre list** — all genres with a description and a count of books in each.
![Genre list](docs/screenshots/genre_list.png)

**Book detail** — full book info, average rating, the reader's own shelves
and rating/review form, and recent reviews from other readers.
![Book detail](docs/screenshots/book_detail.png)

**Author detail** — author bio and all their books; the photo turns
grayscale automatically for authors who have passed away.
![Author detail](docs/screenshots/author_detail.png)

**Genre detail** — all books belonging to a single genre.
![Genre detail](docs/screenshots/genre_detail.png)

**My library** — the logged-in reader's shelves with the books on each one.
![My library](docs/screenshots/my_library.png)

**New shelf** — a reader can create a custom shelf beyond the default ones.
![New shelf](docs/screenshots/new_shelf.png)

**Reader profile** — the logged-in reader's own info, with an edit option.
![Profile](docs/screenshots/profile.png)

**Registration** — sign-up form, including optional birth date and avatar.
![Register](docs/screenshots/register.png)

## Database schema

![Database schema](docs/db_schema.png)

## Setup

1. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/FedirKiiko/digital-library.git
   cd digital-library
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. (Optional) Load sample data:
   ```bash
   python manage.py loaddata fixture.json
   ```
   All seeded readers use the password `password123`. User `admin` is a
   superuser with staff access.

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/` in your browser.

## Models

- **Reader** — custom user model (`AbstractUser`), with `birth_date` and `avatar`
- **Author** — `first_name`, `last_name`, `pseudonym`, `birth_date`,
  `death_date`, `bio`, `photo`, `country`; `is_alive` is a computed property
- **Genre** — `name`, `description`
- **Book** — `title`, `pages`, `year_published`, `publisher`, `cover_image`;
  many-to-many with `Author` and `Genre`
- **Shelf** — a reader's custom book collection (many-to-many with `Book`)
- **ReaderBook** — one record per reader/book pair, holding `status`,
  `rating`, and `review`

## License

This project was built for educational purposes as part of the Mate Academy
Python course.
