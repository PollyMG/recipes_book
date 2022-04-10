from datetime import date
from django import test as django_test
from django.contrib.auth import get_user_model

from recipes_book.main.models import Category, Recipe, Comment

UserModel = get_user_model()


class CategoryTests(django_test.TestCase):
    VALID_CATEGORY_TYPE = {
        'type': 'Other',
    }

    def test_category_type(self):
        category = Category(**self.VALID_CATEGORY_TYPE)

        expected_type = f'{self.VALID_CATEGORY_TYPE["type"]}'

        self.assertEqual(expected_type, category.__str__())


class RecipeTests(django_test.TestCase):
    VALID_RECIPE_DATA = {
        'title': 'Recipe',
        'image_url': 'http://test.picturerecipe/url.png',
        'time_cook': '30',
        'publication_date': date(2022, 4, 10),
    }

    def test_title_max_length(self):
        recipe = Recipe(**self.VALID_RECIPE_DATA)
        max_length = recipe._meta.get_field('title').max_length
        self.assertEqual(max_length, 30)

    def test_image_url_label(self):
        recipe = Recipe(**self.VALID_RECIPE_DATA)
        image_url_label = recipe._meta.get_field('image_url').verbose_name
        self.assertEqual(image_url_label, 'Image URL')

    def test_user_label(self):
        recipe = Recipe(**self.VALID_RECIPE_DATA)
        user_label = recipe._meta.get_field('user').verbose_name
        self.assertEqual(user_label, 'Author')

    def test_recipe_title__when_valid_expect_correct_name(self):
        recipe = Recipe(**self.VALID_RECIPE_DATA)

        expected_recipe_title = f'{self.VALID_RECIPE_DATA["title"]}'

        self.assertEqual(expected_recipe_title, recipe.__str__())


class CommentTest(django_test.TestCase):
    VALID_COMMENT_DATA = {
        'body': 'Good',
        'created': date(2022, 4, 8),
    }

    def test_comment_label(self):
        comment = Comment(**self.VALID_COMMENT_DATA)

        expected_comment_label = f'{self.VALID_COMMENT_DATA["body"]}'

        self.assertEqual(expected_comment_label, comment.__str__())

    def test_user_label(self):
        comment = Comment(**self.VALID_COMMENT_DATA)
        user_label = comment._meta.get_field('user').verbose_name
        self.assertEqual(user_label, 'Author')

    def test_body_label(self):
        comment = Comment(**self.VALID_COMMENT_DATA)
        body_label = comment._meta.get_field('body').verbose_name
        self.assertEqual(body_label, 'Your comment')