# Generated by Django 5.2.3 on 2025-06-29 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_userprofile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='fare',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
