from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta




TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]

class User(AbstractUser):

    pass
class Transaction(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)  # 20 caractères, c'est trop court
    name=models.CharField(max_length=10,default="no_name")
    def serialize(self):
        return {"id":self.id,
                "transaction_type":self.transaction_type,
                "category":self.category,
                "date":self.date,
                "amount":self.amount,
                "description":self.description,
                "name":self.name}
