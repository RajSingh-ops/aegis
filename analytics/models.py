from django.db import models

class Deviation(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()
    recommended_action = models.TextField()
    
    # Metadata fields
    session_id = models.CharField(max_length=100, blank=True, null=True)
    tool_signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"[{self.severity}] {self.timestamp} - {self.description[:50]}..."
