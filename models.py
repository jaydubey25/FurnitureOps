from django.db import models
from django.contrib.auth.models import User

# Create your models here.
USER_TYPE = {
    ('personal', 'PERSONAL'),
    ('ngo', 'NGO')
}

CITY = {
    ('indore', 'INDORE'),
    ('ujjain', 'UJJAIN'),
    ('rao', 'RAO'),
    ('mhow', 'MHOW'),
    ('dewas', 'DEWAS'),
    ('bhopal', 'BHOPAL')
}

class extendedusers(models.Model):
    userType = models.CharField(max_length=50)
    city = models.CharField(max_length=50, choices=CITY, default='INDORE')
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class extendedNgoRequest(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pinCode = models.CharField(max_length=10)
    contactNumber = models.CharField(max_length=10, default='')
    ngo_id = models.CharField(max_length=4, default='')

class extendedNgoAcceptedRequest(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pinCode = models.CharField(max_length=10)
    contactNumber = models.CharField(max_length=10, default='')
    ngo_id = models.CharField(max_length=4, default='')
    request_id = models.CharField(max_length=4, default='')