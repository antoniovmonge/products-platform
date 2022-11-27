from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

# Models
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


class PublishedManager(models.Manager):
    """
    This class is a manager to retrieve Products as:
    'Product.published.all()'
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=Product.Status.PUBLISHED)


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
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(
        max_length=200,
        unique_for_date="publish",
        db_index=True,
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="products_created",
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to="products/", blank=True, max_length=255)
    description = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    publish = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.UPLOADED
    )
    objects = models.Manager()
    published = PublishedManager()
    users = models.ManyToManyField(CustomUser, related_name="products")

    class Meta:
        ordering = [Lower("name")]
        index_together = (("id", "slug"),)

    def get_absolute_url(self):
        return reverse(
            "catalog:product_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company.name + "-" + self.name)
        super().save(*args, **kwargs)


class ProductDetail(models.Model):
    DECLARED_UNIT_CHOICES = [
        ("m", "meter"),
        ("m3", "m3"),
        ("m2", "m2"),
        ("kg", "kg"),
        ("piece", "piece"),
    ]
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    declared_unit = models.CharField(
        max_length=64,
        null=True,
        choices=DECLARED_UNIT_CHOICES,
        default="m2",
        verbose_name="Declared unit",
    )
    total_co2e_kg_mf = models.FloatField(
        blank=True, null=True, verbose_name="Total CO2e [kg]"
    )
    total_biogenic_co2e = models.FloatField(
        blank=True, null=True, verbose_name="Total Biogenic CO2e [kg]"
    )
    carbon_sorting = models.FloatField(
        blank=True, null=True, verbose_name="Carbon Sorting"
    )
    # unit_sorting = models.CharField(
    #     max_length=64, null=True, blank=True, verbose_name="Unit Sorting"
    # )
    # estimated_carbon = models.BooleanField(
    #     default=False, verbose_name="Estimated Carbon"
    # )
    water_use_kg = models.FloatField(
        blank=True, null=True, verbose_name="Water Use [kg]"
    )
    use_and_maintenance = models.FloatField(
        blank=True, null=True, verbose_name="Use & Maintenance (B1-B5) [kg]"
    )
    # data_source = models.CharField(
    #     max_length=128, null=True, blank=True, verbose_name="Data Source"
    # )
    end_of_life = models.FloatField(
        blank=True,
        null=True,
        verbose_name="End of Life excluding transport (C1, C3, C4) [kg]",
    )
    recycled_content = models.FloatField(
        blank=True, null=True, verbose_name="Recycled Content [%]"
    )
    recyclable_content = models.FloatField(
        blank=True, null=True, verbose_name="Recyclable Content [%]"
    )
    reuse_potential = models.FloatField(
        blank=True, null=True, verbose_name="Re-use Potential [%]"
    )
    odp = models.FloatField(blank=True, null=True, verbose_name="ODP")
    manufacturing = models.FloatField(
        blank=True, null=True, verbose_name="Manufacturing (A1-A3) [kg]"
    )
    on_site_installation = models.FloatField(
        blank=True, null=True, verbose_name="On-site Installation (A5) [kg]"
    )
    # transport_to_site = models.FloatField(
    #     blank=True, null=True, verbose_name="Transport to Site (A4) [kg]"
    # )
    energy_recovery_possibility = models.FloatField(
        blank=True, null=True, verbose_name="Energy Recovery Possibility [%]"
    )

    class Meta:
        ordering = ("product",)

    def __str__(self):
        return f"Details for product: '{self.product.name}'"


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
