# Generated by Django 5.1.6 on 2025-02-26 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '00001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='change',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
