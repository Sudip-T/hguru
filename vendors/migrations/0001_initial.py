# Generated by Django 5.0.2 on 2024-04-08 08:18

import core.validators
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("category_name", models.CharField(max_length=255, unique=True)),
                ("img", models.ImageField(null=True, upload_to="vendors/category/")),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ServiceType",
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
                ("name", models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Vendor",
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
                ("cover_photo", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "company_name",
                    models.CharField(
                        max_length=255,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
                (
                    "contact_number",
                    models.BigIntegerField(
                        unique=True, validators=[core.validators.validate_phone_number]
                    ),
                ),
                (
                    "emergency_contact",
                    models.BigIntegerField(
                        null=True, validators=[core.validators.validate_phone_number]
                    ),
                ),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("description", models.TextField(null=True)),
                (
                    "ratings",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "vendor_status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Pending", "Pending"),
                            ("Verified", "Verified"),
                        ],
                        default="New",
                        max_length=10,
                    ),
                ),
                (
                    "available",
                    models.BooleanField(
                        choices=[(True, "Available"), (False, "Not Available")],
                        default=False,
                    ),
                ),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vendors",
                        to="vendors.category",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vendor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Service",
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
                ("service_name", models.CharField(max_length=255)),
                ("description", models.TextField(null=True)),
                ("price", models.IntegerField()),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="vendors.vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Gallery",
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
                ("image", models.ImageField(upload_to="vendor/gallery/")),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="galleries",
                        to="vendors.vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Facility",
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
                ("facility_name", models.CharField(max_length=255)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="facility",
                        to="vendors.vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Documents",
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
                ("document_type", models.CharField(max_length=255)),
                ("document", models.ImageField(upload_to="vendor/document/")),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "pan_number",
                    models.BigIntegerField(
                        null=True,
                        unique=True,
                        validators=[core.validators.validate_pan_number],
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="vendors.vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VendorAddress",
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
                ("district", models.CharField(max_length=100)),
                ("country", models.CharField(default="Nepal", max_length=100)),
                ("province", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "address_line",
                    models.TextField(
                        help_text="Municipality, Ward No, Tole", max_length=200
                    ),
                ),
                ("nearest_landmark", models.TextField(blank=True, null=True)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address",
                        to="vendors.vendor",
                    ),
                ),
            ],
        ),
    ]
