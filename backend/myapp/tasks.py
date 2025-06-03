import pandas as pd
from celery import shared_task
from .models import Customer, Loan

@shared_task
def ingest_customer_data(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': row['phone_number'],
                'monthly_salary': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'current_debt': row['current_debt'],
            }
        )

@shared_task
def ingest_loan_data(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Loan.objects.update_or_create(
            loan_id=row['loan id'],
            defaults={
                'customer_id': row['customer id'],
                'loan_amount': row['loan amount'],
                'tenure': row['tenure'],
                'interest_rate': row['interest rate'],
                'monthly_repayment': row['monthly repayment (emi)'],
                'emis_paid_on_time': row['EMIs paid on time'],
                'start_date': row['start date'],
                'end_date': row['end date'],
            }
        )
        