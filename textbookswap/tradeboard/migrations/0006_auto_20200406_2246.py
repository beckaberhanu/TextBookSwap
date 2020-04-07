# Generated by Django 3.0.3 on 2020-04-06 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeboard', '0005_merge_20200406_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('Other', 'Other'), ('Textbook', 'Textbook')], default='Other', max_length=50),
        ),
        migrations.AddField(
            model_name='post',
            name='price',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='swappable',
            field=models.BooleanField(default=False),
        ),
    ]
