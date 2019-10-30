from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    OCCUPATION_CHOOSES = [
        ('D', 'Врач'),
        ('N', 'Медперсонал'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(choices=OCCUPATION_CHOOSES, max_length=1)

