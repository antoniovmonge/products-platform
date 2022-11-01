from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

# from django.contrib.auth import get_user_model
from pplatform.users.models import Company, CustomUser


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("catalog:product_list_by_category", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "UP", "Uploaded"
        PUBLISHED = "PB", "Published"

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    company = models.ForeignKey(
        Company, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="products_created",
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.UPLOADED
    )

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.id, self.slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company.name + "-" + self.name)
        super().save(*args, **kwargs)


class Content(models.Model):
    product = models.ForeignKey(
        Product, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")


class ItemBase(models.Model):
    company = models.ForeignKey(
        Company, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f"catalog/content/{self._meta.model_name}.html", {"item": self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    url = models.URLField()
