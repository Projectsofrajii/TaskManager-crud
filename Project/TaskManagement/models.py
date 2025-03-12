from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Index

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]  #[(key,value)]

    title = models.CharField(max_length=255,verbose_name="Project Title")
    title_id = models.CharField(max_length=45,unique=True,blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to authenticated user
    
    def save(self, *args, **kwargs):
        if not self.title_id:  # Generate title_id only if it's empty
            last_task = Task.objects.order_by('-id').first()  # Get the latest task
            
            if last_task and last_task.title_id:
                last_number = int(last_task.title_id[3:])  # Extract number from 'TIDXXX'
                new_number = last_number + 1
            else:
                new_number = 0  # First record starts from TID000
            
            self.title_id = f'TID{new_number:03d}'  # Format as TID000, TID001, TID002...

        super().save(*args, **kwargs)  # Save the object

    def __str__(self):
        return f"{self.title_id} - {self.title}"
    
    class Meta:
        db_table = 'taskmaster'
        indexes = [Index(fields=['status']), ] # ✅ Indexing the `status` field for fast lookups
        

# Signal to update `updated_at` timestamp on save
@receiver(pre_save, sender=Task)
def update_timestamp(sender, instance, **kwargs):
    if instance.title:
        instance.updated_at = now()
        print('update_timestamp',update_timestamp)
