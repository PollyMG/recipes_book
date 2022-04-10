from datetime import date
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from recipes_book.accounts.models import Profile, RecipesUser

UserModel = get_user_model()


class ProfileTests(django_test.TestCase):
    VALID_PROFILE_DATA = {
        'first_name': 'Polly',
        'last_name': 'Yankova',
    }

    def test_profile_full_name__when_valid_expect_correct_name(self):
        profile = Profile(**self.VALID_PROFILE_DATA)

        expected_full_name = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'

        self.assertEqual(expected_full_name, profile.__str__())

    def test_first_name_max_length(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        max_length = profile._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 30)

    def test_last_name_max_length(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        max_length = profile._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 30)


class RecipesUserTests(django_test.TestCase):
    VALID_USER_DATA = {
        'username': 'pollyg',
        'password': '123qwe',
    }

    def test_username_max_length(self):
        profile = RecipesUser(**self.VALID_USER_DATA)
        max_length = profile._meta.get_field('username').max_length
        self.assertEqual(max_length, 25)


class ProfileDetailsViewTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qew'
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'http://test.picture/url.png',
        'date_of_birth': date(1990, 4, 13),
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return user, profile

    def test_expect_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))
        self.assertTemplateUsed('profile_details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',
        }
        self.__create_user(**credentials)
        self.client.login(**credentials)

        response = self.__get_response_for_profile(profile)

        self.assertFalse(response.context['is_owner'])


