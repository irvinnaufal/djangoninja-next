from django.utils import timezone
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)  # ✅ Soft delete flag
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Remove default
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'warehouse\".\"item'


    def __str__(self):
        return self.name
