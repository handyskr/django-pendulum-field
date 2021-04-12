# Generated by Django 3.2 on 2021-04-12 16:49

from django.db import migrations, models
import django_pendulum_field.model


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Something",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("some_dt", django_pendulum_field.model.PendulumField()),
            ],
        ),
        migrations.CreateModel(
            name="SomethingWithAutoNow",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("some_dt", django_pendulum_field.model.PendulumField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SomethingWithAutoNowAdd",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("dummy_field", models.CharField(default="hi", max_length=4)),
                ("some_dt", django_pendulum_field.model.PendulumField(auto_now_add=True)),
            ],
        ),
    ]