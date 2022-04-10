from django.contrib.auth import mixins as auth_mixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from recipes_book.main.forms import CreateRecipeForm, CommentForm
from recipes_book.main.models import Recipe, Comment


class RedirectToDashboard:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'home_page.html'


class DashboardView(views.ListView):
    model = Recipe
    template_name = 'dashboard.html'
    context_object_name = 'recipes'


class CreateRecipeView(auth_mixin.LoginRequiredMixin, views.CreateView):
    template_name = 'recipe_create.html'
    form_class = CreateRecipeForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditRecipeView(views.UpdateView):
    model = Recipe
    template_name = 'recipe_edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('details recipe', kwargs={'pk': self.object.id})


class CommentRecipeView(views.CreateView):
    form_class = CommentForm
    template_name = 'comment_recipe.html'

    def get_success_url(self):
        return reverse_lazy('details recipe', kwargs={'pk': self.object.recipe_id})

    def form_valid(self, form):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        comment = Comment(
            body=form.cleaned_data['body'],
            recipe=recipe,
            user=self.request.user,)

        comment.save()
        return redirect('details recipe', recipe.id)


class DeleteRecipeView(views.DeleteView):
    model = Recipe
    template_name = 'delete_recipe.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard')


class RecipeDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Recipe
    template_name = 'recipe_details.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.object.user == self.request.user
        context.update({
            'is_owner': self.object.user_id == self.request.user.id
        })

        return context


def error_404(request, exception):
    return render(request, '404_error.html')

