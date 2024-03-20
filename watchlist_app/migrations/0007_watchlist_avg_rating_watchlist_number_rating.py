# Generated by Django 4.2 on 2024-03-11 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("watchlist_app", "0006_review_reviewer"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="avg_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="watchlist",
            name="number_rating",
            field=models.IntegerField(default=0),
        ),
    ]
