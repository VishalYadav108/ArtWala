# Generated by Django 5.2.4 on 2025-07-03 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chapter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("country", models.CharField(default="India", max_length=100)),
                ("description", models.TextField()),
                (
                    "cover_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="chapter_images/"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("contact_email", models.EmailField(blank=True, max_length=254)),
                ("contact_phone", models.CharField(blank=True, max_length=15)),
                ("social_links", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Chapter",
                "verbose_name_plural": "Chapters",
                "db_table": "chapters",
            },
        ),
        migrations.CreateModel(
            name="ChapterEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=250)),
                ("description", models.TextField()),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("exhibition", "Exhibition"),
                            ("workshop", "Workshop"),
                            ("meetup", "Meetup"),
                            ("competition", "Competition"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("location", models.CharField(max_length=200)),
                (
                    "max_participants",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "registration_fee",
                    models.DecimalField(decimal_places=2, default=0, max_digits=8),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="event_images/"),
                ),
                ("is_public", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "chapter_events",
            },
        ),
        migrations.CreateModel(
            name="ChapterMembership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "chapter_memberships",
            },
        ),
        migrations.CreateModel(
            name="EventRegistration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("registered_at", models.DateTimeField(auto_now_add=True)),
                ("attended", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "event_registrations",
            },
        ),
    ]
