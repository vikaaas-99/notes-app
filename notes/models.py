from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " - " + self.user.username
    

class LogNoteHistory(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)


class SharedNotes(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_with")
    shared_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note.title + " - " + self.shared_with.username

