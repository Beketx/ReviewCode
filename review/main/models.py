from django.db import models
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

class Company(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):

    RATING_OPTIONS = ((1, 'One stars'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars'))

    rating = models.IntegerField(choices=RATING_OPTIONS)
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=100000)
    ip_address = models.CharField(max_length=45)
    submission_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, related_name='reviews', on_delete=models.PROTECT)
    reviewer = models.ForeignKey(Token, related_name='reviews', on_delete=models.PROTECT)