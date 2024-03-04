from django.db import models
from django.contrib.auth.models import User
from SchedulesApp.models import Schedule

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='tickets')
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Ticket for {self.user.username} - {self.schedule.line.name}, Departure: {self.schedule.departure_time}"
