from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, logout

from recipes_book.accounts.forms import CreateProfileForm
from recipes_book.accounts.models import Profile, RecipesUser
from recipes_book.main.views import RedirectToDashboard


class UserRegisterView(RedirectToDashboard, views.CreateView):
    form_class = CreateProfileForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('dashboard')


class UserLoginView(auth_views.LoginView):
    template_name = 'login_page.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class EditProfileView(views.UpdateView):
    model = Profile
    template_name = 'profile_edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'change_password.html'


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user

        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })

        return context


class DeleteProfileView(views.DeleteView):
    model = RecipesUser
    template_name = 'profile_delete.html'
    success_url = reverse_lazy('show index')


def user_logout_view(request):
    logout(request)
    return redirect('show index')
