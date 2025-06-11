from django.contrib import admin
from myapp.models import Customer, Loan

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_ID', 'first_name', 'last_name', 'age', 'phone_number', 'monthly_income', 'approved_limit')
    search_fields = ('first_name', 'last_name', 'phone_number')
    
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'customer', 'loan_amount', 'tenure', 'interest_rate', 'monthly_payment', 'emis_paid_on_time', 'start_date', 'end_date')
    search_fields = ['loan_id']