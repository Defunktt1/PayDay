from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from register.forms import User


# Create your models here.
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    day = models.DateField()
    hours = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    work_description = models.CharField(max_length=200)
    create_date = models.TimeField()

    def __str__(self):
        return self.work_description
