from django.urls import path

from recipes_book.main.views import HomeView, DashboardView, CreateRecipeView, EditRecipeView, DeleteRecipeView, \
    RecipeDetailsView, CommentRecipeView

urlpatterns = (
    path('', HomeView.as_view(), name='show index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('create/', CreateRecipeView.as_view(), name='create recipe'),
    path('edit/<int:pk>/', EditRecipeView.as_view(), name='edit recipe'),
    path('delete/<int:pk>/', DeleteRecipeView.as_view(), name='delete recipe'),
    path('details/<int:pk>/', RecipeDetailsView.as_view(), name='details recipe'),
    path('comment/<int:pk>/', CommentRecipeView.as_view(), name='comment recipe'),
)

