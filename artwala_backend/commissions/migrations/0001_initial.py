# Generated by Django 5.2.4 on 2025-07-03 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("artists", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommissionContract",
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
                ("final_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("start_date", models.DateField()),
                ("expected_completion_date", models.DateField()),
                ("terms_agreed", models.TextField()),
                ("client_signed", models.BooleanField(default=False)),
                ("artist_signed", models.BooleanField(default=False)),
                ("client_signed_at", models.DateTimeField(blank=True, null=True)),
                ("artist_signed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "commission_contracts",
            },
        ),
        migrations.CreateModel(
            name="CommissionMilestone",
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
                ("description", models.TextField()),
                ("order", models.PositiveIntegerField()),
                (
                    "percentage",
                    models.PositiveIntegerField(help_text="Percentage of total work"),
                ),
                (
                    "payment_percentage",
                    models.PositiveIntegerField(
                        help_text="Percentage of total payment"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("approved", "Approved"),
                            ("revision_requested", "Revision Requested"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("progress_images", models.JSONField(blank=True, default=list)),
                ("client_feedback", models.TextField(blank=True)),
                ("due_date", models.DateField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "commission_milestones",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="CommissionProposal",
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
                (
                    "proposed_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "estimated_completion_time",
                    models.PositiveIntegerField(help_text="Estimated days to complete"),
                ),
                ("proposal_description", models.TextField()),
                ("terms_and_conditions", models.TextField()),
                ("sample_images", models.JSONField(blank=True, default=list)),
                ("milestone_plan", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "commission_proposals",
            },
        ),
        migrations.CreateModel(
            name="CommissionReview",
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
                (
                    "rating",
                    models.PositiveIntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
                    ),
                ),
                ("comment", models.TextField()),
                ("would_recommend", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "commission_reviews",
            },
        ),
        migrations.CreateModel(
            name="CommissionPayment",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("payment_method", models.CharField(max_length=50)),
                ("transaction_id", models.CharField(blank=True, max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                            ("refunded", "Refunded"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "milestone",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commissions.commissionmilestone",
                    ),
                ),
            ],
            options={
                "db_table": "commission_payments",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CommissionRequest",
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
                ("description", models.TextField()),
                (
                    "commission_type",
                    models.CharField(
                        choices=[
                            ("painting", "Painting"),
                            ("sculpture", "Sculpture"),
                            ("mural", "Mural"),
                            ("portrait", "Portrait"),
                            ("digital_art", "Digital Art"),
                            ("illustration", "Illustration"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("budget_min", models.DecimalField(decimal_places=2, max_digits=10)),
                ("budget_max", models.DecimalField(decimal_places=2, max_digits=10)),
                ("deadline", models.DateField()),
                ("dimensions", models.CharField(blank=True, max_length=100)),
                ("reference_images", models.JSONField(blank=True, default=list)),
                ("additional_requirements", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("submitted", "Submitted"),
                            ("under_review", "Under Review"),
                            ("accepted", "Accepted"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("delivered", "Delivered"),
                            ("rejected", "Rejected"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="submitted",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commission_requests",
                        to="artists.artistprofile",
                    ),
                ),
            ],
            options={
                "db_table": "commission_requests",
                "ordering": ["-created_at"],
            },
        ),
    ]
