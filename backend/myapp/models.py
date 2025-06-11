from django.db import models

# myapp/models.py
class Customer(models.Model):
    customer_ID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=301)
    last_name = models.CharField(max_length=301)
    age = models.IntegerField()
    phone_number = models.BigIntegerField(unique=True)
    monthly_income = models.IntegerField()
    approved_limit = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_id = models.CharField(max_length=5000)
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_payment = models.FloatField()
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for {self.customer.first_name} {self.customer.last_name}"
