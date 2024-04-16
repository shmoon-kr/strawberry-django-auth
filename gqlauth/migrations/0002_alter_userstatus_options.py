# Generated by Django 4.1.7 on 2023-05-07 15:38

from django.contrib.auth import get_user_model
from django.db import migrations


def set_userstatus(apps, schema_editor):
    # Setting default values for existing data
    userstatus = apps.get_model("gqlauth", "userstatus")
    User = get_user_model()
    for user in User.objects.all():
        userstatus.objects.create(id=user.id, verified=True, archived=False, user_id=user.id)


class Migration(migrations.Migration):
    dependencies = [
        ("gqlauth", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userstatus",
            options={"verbose_name_plural": "User statuses"},
        ),
        migrations.RunPython(set_userstatus),
    ]
