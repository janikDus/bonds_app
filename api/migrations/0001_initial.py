# Generated by Django 5.0.6 on 2024-07-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BondPost",
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
                ("bond_name", models.CharField(max_length=50)),
                ("isin", models.CharField(max_length=12)),
                ("bond_value", models.BigIntegerField()),
                ("interest_rate", models.FloatField()),
                ("purchase_date", models.DateTimeField()),
                ("due_date", models.DateTimeField()),
                ("yields_freq", models.IntegerField()),
            ],
        ),
    ]
