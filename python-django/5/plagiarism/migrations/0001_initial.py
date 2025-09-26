import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("submissions", "0002_alter_submission_code_file_alter_submission_language"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlagiarismResult",
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
                    "similarity_score",
                    models.FloatField(
                        help_text="Similarity percentage between 0 and 100"
                    ),
                ),
                ("flagged", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "similar_submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="similar_to_results",
                        to="submissions.submission",
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plagiarism_results",
                        to="submissions.submission",
                    ),
                ),
            ],
            options={
                "unique_together": {("submission", "similar_submission")},
            },
        ),
    ]
