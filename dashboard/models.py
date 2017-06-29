from django.db import models

from geoposition.fields import GeopositionField

# Create your models here.
class user(models.Model):
	username=models.CharField(max_length=20,primary_key=True)

	# password is stored as plain text!!!
	# change during production
	password=models.CharField(max_length=30,blank=False)
	email=models.CharField(max_length=200)
	phone_number=models.CharField(max_length=15)
	first_name=models.CharField(max_length=40)
	last_name=models.CharField(max_length=40,blank=True,null=True)
	age=models.IntegerField(default=0)

class Place(models.Model):
	name=models.CharField(max_length=50)
	description=models.CharField(max_length=50)
	position=GeopositionField()