# Generated by Django 2.0.4 on 2018-04-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyp_project', '0012_auto_20180430_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleanmessage',
            name='totalTweets',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
