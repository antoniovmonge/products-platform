# Generated by Django 4.0.8 on 2022-11-01 11:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_file_company_alter_image_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('UP', 'Uploaded'), ('PB', 'Published')], default='UP', max_length=2),
        ),
    ]
