# Generated by Django 4.0.8 on 2022-10-31 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='catalog.company'),
        ),
        migrations.AlterField(
            model_name='image',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='catalog.company'),
        ),
        migrations.AlterField(
            model_name='text',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='catalog.company'),
        ),
        migrations.AlterField(
            model_name='video',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='catalog.company'),
        ),
    ]
