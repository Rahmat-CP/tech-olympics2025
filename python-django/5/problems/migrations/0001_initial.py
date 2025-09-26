import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Problem",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("input_description", models.TextField()),
                ("output_description", models.TextField()),
                (
                    "time_limit",
                    models.FloatField(default=1.0, help_text="Time limit in seconds"),
                ),
                (
                    "memory_limit",
                    models.IntegerField(default=128, help_text="Memory limit in MB"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TestCase",
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
                ("input_data", models.TextField()),
                ("expected_output", models.TextField()),
                ("is_sample", models.BooleanField(default=False)),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="testcases",
                        to="problems.problem",
                    ),
                ),
            ],
        ),
    ]
