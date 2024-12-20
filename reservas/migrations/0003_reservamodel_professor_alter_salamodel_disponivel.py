# Generated by Django 4.2.3 on 2024-12-17 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_professor"),
        ("reservas", "0002_reservamodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservamodel",
            name="professor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservas",
                to="users.professor",
            ),
        ),
        migrations.AlterField(
            model_name="salamodel",
            name="disponivel",
            field=models.BooleanField(default=True),
        ),
    ]
