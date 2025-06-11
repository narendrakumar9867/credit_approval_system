import pandas as pd
from django.core.management.base import BaseCommand
from myapp.models import Customer, Loan
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Import customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR, 'data')

        # ---------------- Import Customers ----------------
        customer_file = os.path.join(data_dir, "customer_data.xlsx")
        try:
            customer_df = pd.read_excel(customer_file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Customer file not found: {customer_file}"))
            return

        for _, row in customer_df.iterrows():
            customer, created = Customer.objects.get_or_create(
                customer_ID=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'age': row['Age'],
                    'phone_number': row['Phone Number'],
                    'monthly_income': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit']
                }
            )
        self.stdout.write(self.style.SUCCESS('✅ Customer data imported successfully'))

        # ---------------- Import Loans ----------------
        loan_file = os.path.join(data_dir, "loan_data.xlsx")
        try:
            loan_df = pd.read_excel(loan_file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Loan file not found: {loan_file}"))
            return

        for _, row in loan_df.iterrows():
            try:
                customer = Customer.objects.get(customer_ID=row['Customer ID'])
                Loan.objects.create(
                    customer=customer,
                    loan_id=row['Loan ID'],
                    loan_amount=row['Loan Amount'],
                    tenure=row['Tenure'],
                    interest_rate=row['Interest Rate'],
                    monthly_payment=row['Monthly payment'],
                    emis_paid_on_time=row['EMIs paid on Time'],
                    start_date=row['Date of Approval'],
                    end_date=row['End Date']
                )
            except Customer.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️ Customer ID {row['Customer ID']} not found. Loan skipped."))

        self.stdout.write(self.style.SUCCESS('✅ Loan data imported successfully'))
