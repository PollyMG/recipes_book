from django import forms

from recipes_book.main.helpers import BootstrapFormMixin
from recipes_book.main.models import Recipe, Comment


class CreateRecipeForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        recipe = super().save(commit=False)

        recipe.user = self.user
        if commit:
            recipe.save()

        return recipe

    class Meta:
        model = Recipe
        fields = ('title', 'image_url', 'intro', 'description', 'time_cook', 'category')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter recipe title',
                }
            ),
            'image_url': forms.TextInput(
                attrs={
                    'placeholder': 'Enter image URL'
                }
            ),
            'intro': forms.TextInput(
                attrs={
                    'placeholder': 'Enter intro text',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Enter description text',
                }
            ),
            'time_cook': forms.TextInput(
                attrs={
                    'placeholder': 'Enter time to cook',
                }
            ),
        }


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'


class DeleteRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        Recipe.objects.all().delete()
        return self.instance

    class Meta:
        model = Recipe
        fields = '__all__'


class DetailsRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.TextInput(
                attrs={
                    'placeholder': 'Write your comment here...',
                }
            ),
        }


