from django.db import models

# myapp/models.py
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    monthly_income = models.IntegerField()
    approved_limit = models.IntegerField()
    phone_number = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_id = models.CharField(max_length=20)
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_repayment = models.FloatField()
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
