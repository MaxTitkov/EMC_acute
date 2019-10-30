from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Patient(models.Model):
    fullname = models.CharField(max_length=100, unique=True, verbose_name='Ф.И.О.')
    dob = models.DateField(verbose_name='Дата рождения')
    room = models.SmallIntegerField(blank=True, null=True, verbose_name='Номер палаты')
    is_active = models.BooleanField(default=False, verbose_name='Госпитализирован в данный момент?')
    hided = models.BooleanField(default=False)
    
    srisk = models.BooleanField(default=False, verbose_name='Суицидальный риск')
    self_harm = models.BooleanField(default=False, verbose_name='Самоповреждения')
    drisk = models.BooleanField(default=False, verbose_name='Риск падения')

    def __str__(self):
        return self.fullname

    def age(self):
        import datetime
        return int((datetime.date.today() - self.dob).days / 365.25  )
    

class Info(models.Model):

    S_RISK_CHOICES = [
        (0, "Нет"),
        (1, "Низкий"),
        (2, "Высокий"),
    ]

    current_date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    suicidal_risk = models.SmallIntegerField(choices=S_RISK_CHOICES, blank=False, null=False)
    bathroom_time = models.PositiveSmallIntegerField(blank=True, null=True)
    record = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return ('{date} - {patient}').format(date=self.current_date, patient=self.patient)

    class Meta:
        ordering = ['-current_date']

