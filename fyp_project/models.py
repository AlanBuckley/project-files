from django.db import models

class Tweets(models.Model):
    date= models.DateTimeField()
    message= models.CharField(max_length=280)
    cleanMessage = models.CharField(max_length=280, blank=True)

    def __unicode__(self):
        return str(self.date)


class MLCache(models.Model):
    affective_counts_cyberbullying_json = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)

class CleanMessage(models.Model):
    recall = models.TextField(max_length=255, blank=True)
    precision = models.TextField(max_length=255, blank=True)
    true_positives = models.TextField(max_length=255, blank=True)
    false_positives = models.TextField(max_length=255, blank=True)
    true_negatives = models.TextField(max_length=255, blank=True)
    false_negatives = models.TextField(max_length=255, blank=True)
    totalTweets = models.TextField(max_length=255, blank=True)
    fScore = models.TextField(max_length=255, blank=True)


    def __unicode__(self):
        return str(self.id)

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

class Meta:
    db_table = 'auth_user'


    def __unicode__(self):
        return str(self.id)
