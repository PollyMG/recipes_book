from django.contrib import admin

from recipes_book.accounts.models import Profile, RecipesUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')


@admin.register(RecipesUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff')
    filter_horizontal = ("groups", "user_permissions")
