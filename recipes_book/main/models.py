from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DO_NOTHING

UserModel = get_user_model()


class Category(models.Model):
    CHOCOLATE = "Chocolate"
    WHITE_CAKE = "White_Cake"
    CANDY = "Candy"
    CHEESECAKE = "Cheesecake"
    CHRISTMAS = "Christmas"
    OTHER = "Other"

    TYPES = [(x, x) for x in (CHOCOLATE, WHITE_CAKE, CANDY, CHEESECAKE, CHRISTMAS, OTHER)]
    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.type


class Recipe(models.Model):
    TITLE_MAX_LEN = 30

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        unique=True,
    )
    image_url = models.URLField(
        verbose_name='Image URL',
    )
    intro = models.TextField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    time_cook = models.IntegerField()

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )
    category = models.ForeignKey(Category, on_delete=DO_NOTHING,)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='Author',
    )

    class Meta:
        ordering = ('-publication_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='Your comment')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='Author',
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body
