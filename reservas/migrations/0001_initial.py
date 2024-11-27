# Generated by Django 4.2.3 on 2024-11-27 11:47

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SalaModel",
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
                ("numero", models.IntegerField()),
                ("bloco", models.IntegerField()),
                ("capacidade", models.IntegerField()),
                ("tipo", models.CharField(max_length=20)),
                ("disponivel", models.BooleanField()),
            ],
            options={
                "verbose_name": "Sala",
                "verbose_name_plural": "Salas",
            },
        ),
    ]