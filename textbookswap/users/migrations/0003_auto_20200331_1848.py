# Generated by Django 3.0.3 on 2020-03-31 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='wishlist',
            new_name='posts',
        ),
    ]