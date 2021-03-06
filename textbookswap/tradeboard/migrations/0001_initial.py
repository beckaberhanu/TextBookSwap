# Generated by Django 3.0.3 on 2020-05-06 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tradeboard.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('ISBN', models.CharField(max_length=13, validators=[tradeboard.models.Post.validate_ISBN])),
                ('author', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('image', models.ImageField(default='default_book.png', upload_to='book_pics')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('edition', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('price', models.PositiveSmallIntegerField(default=0)),
                ('swappable', models.BooleanField(default=False)),
                ('transaction_state', models.CharField(choices=[('In progress', 'In progress'), ('Complete', 'Complete')], default='In progress', max_length=50)),
                ('post_type', models.CharField(choices=[('Other', 'Other'), ('Textbook', 'Textbook')], default='Other', max_length=50)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
    ]
