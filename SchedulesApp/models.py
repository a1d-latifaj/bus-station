from django.db import models
from BusLinesApp.models import Line

class Schedule(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='schedules')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.line.name} - Departure: {self.departure_time}, Arrival: {self.arrival_time}"
