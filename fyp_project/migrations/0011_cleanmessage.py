# Generated by Django 2.0.4 on 2018-04-28 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyp_project', '0010_tweets_cleanmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleanMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cleanmessage', models.TextField(blank=True, max_length=255)),
            ],
        ),
    ]
