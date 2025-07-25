# Generated by Django 5.2.3 on 2025-06-28 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0002_recharge_ticket"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="age",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="mobile",
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
        ),
    ]
