import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Import data from CSV into database'

    def handle(self, *args, **options):
        data_dir = Path(settings.BASE_DIR) / 'static' / 'data'

        self.import_categories(data_dir / 'category.csv')
        self.import_genres(data_dir / 'genre.csv')
        self.import_titles(data_dir / 'titles.csv')
        self.import_genre_title(data_dir / 'genre_title.csv')
        self.import_users(data_dir / 'users.csv')
        self.import_reviews(data_dir / 'review.csv')
        self.import_comments(data_dir / 'comments.csv')
        self.stdout.write(self.style.SUCCESS('Данные загружены'))

    def import_categories(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                    }
                )

    def import_genres(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                    }
                )

    def import_titles(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': row['year'],
                        'category': category,
                    }
                )

    def import_genre_title(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)

    def import_users(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'bio': row['bio'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name']
                    }
                )

    def import_reviews(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                author = User.objects.get(id=row['author'])
                Review.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'text': row['text'],
                        'score': row['score'],
                        'pub_date': row['pub_date'],
                        'title': title,
                        'author': author,
                    }
                )

    def import_comments(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                review = Review.objects.get(id=row['review_id'])
                author = User.objects.get(id=row['author'])
                Comment.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'text': row['text'],
                        'pub_date': row['pub_date'],
                        'review': review,
                        'author': author,
                    }
                )
