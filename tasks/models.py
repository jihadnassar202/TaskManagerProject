from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Represents a task in the system with status, owner, assignee and due date.
    """
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_by = models.ForeignKey(
        User,
        related_name='tasks_created',
        on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        User,
        related_name='tasks_assigned',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


# Create your models here.
