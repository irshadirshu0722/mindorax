# models.py
from django.db import models


class FailedTaskAlert(models.Model):
    class Status(models.TextChoices):
        PENDING  = "pending",  "Pending Review"
        RESOLVED = "resolved", "Resolved"
        IGNORED  = "ignored",  "Ignored"

    task_name    = models.CharField(max_length=255)
    payload      = models.JSONField()            # exact args that failed
    error_message = models.TextField()
    traceback    = models.TextField(blank=True)
    status       = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at   = models.DateTimeField(auto_now_add=True)
    resolved_at  = models.DateTimeField(null=True, blank=True)
    resolved_by  = models.ForeignKey(
        "users.User", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="resolved_alerts",
    )
    notes = models.TextField(blank=True)  # admin can leave notes

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Failed Task Alert"

    def __str__(self):
        return f"[{self.status}] {self.task_name} @ {self.created_at:%Y-%m-%d %H:%M}"