import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("problems", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
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
                ("code_file", models.FileField(upload_to="submissions/")),
                (
                    "language",
                    models.CharField(
                        choices=[("py", "Python"), ("cpp", "C++"), ("java", "Java")],
                        max_length=10,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "در انتظار"),
                            ("RUNNING", "در حال اجرا"),
                            ("ACCEPTED", "پاس شده"),
                            ("WRONG_ANSWER", "پاسخ نادرست"),
                            ("RUNTIME_ERROR", "خطای زمان اجرا"),
                            ("COMPILATION_ERROR", "خطای کامپایل"),
                            ("TIME_LIMIT_EXCEEDED", "پایان زمان مجاز"),
                            ("FAILED", "ناموفق"),
                        ],
                        default="PENDING",
                        max_length=30,
                    ),
                ),
                ("output", models.TextField(blank=True, null=True)),
                ("error", models.TextField(blank=True, null=True)),
                ("execution_time", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="problems.problem",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
