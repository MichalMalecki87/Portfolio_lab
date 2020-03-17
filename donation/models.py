from django.contrib.auth.models import User
from django.db import models

# Create your models here.
INSTITUTION_TYPES = ((1, 'fundacja'), (2, 'organizacja pozarządowa'), (3, 'zbiórka lokalna'))


class Category(models.Model):
    name = models.CharField(max_length=100)


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type_inst = models.IntegerField(choices=INSTITUTION_TYPES, default=1)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.DO_NOTHING)
