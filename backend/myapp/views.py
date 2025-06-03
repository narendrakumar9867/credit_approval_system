from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerRegisterSerializer
from .serializers import EligibilityCheckSerializer
from .serializers import LoanDetailSerializer
from .serializers import CustomerLoanListSerializer
import uuid
from datetime import date, timedelta
from .models import Customer, Loan
from .serializers import CreateLoanSerializer

class RegisterCustomerView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            response_data = {
                "customer_id": customer.id,
                "name": f"{customer.first_name} {customer.last_name}",
                "age": customer.age,
                "monthly_income": customer.monthly_income,
                "approved_limit": customer.approved_limit,
                "phone_number": customer.phone_number,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckEligibilityView(APIView):
    def post(self, request):
        serializer = EligibilityCheckSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            customer_id = data["customer_id"]
            loan_amount = data["loan_amount"]
            interest_rate = data["interest_rate"]
            tenure = data["tenure"]

            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

            loans = customer.loans.all()

            current_year = date.today().year
            total_loans = loans.count()
            total_paid_on_time = sum(l.emis_paid_on_time for l in loans)
            current_year_loans = loans.filter(start_date__year=current_year).count()
            approved_volume = sum(l.loan_amount for l in loans)
            total_emi = sum(l.monthly_repayment for l in loans)
            current_total_debt = sum(l.loan_amount for l in loans)

            if current_total_debt > customer.approved_limit:
                credit_score = 0
            else:
                credit_score = 100
                credit_score -= (total_loans * 5)
                credit_score += total_paid_on_time * 0.5
                credit_score += current_year_loans * 2
                credit_score -= (approved_volume / 1000000) 
                credit_score = max(0, min(credit_score, 100))

            approval = False
            corrected_interest_rate = interest_rate

            if total_emi + (loan_amount / tenure) > 0.5 * customer.monthly_income:
                approval = False
            else:
                if credit_score > 50:
                    approval = True
                elif 30 < credit_score <= 50:
                    if interest_rate >= 12:
                        approval = True
                    else:
                        corrected_interest_rate = 12
                elif 10 < credit_score <= 30:
                    if interest_rate >= 16:
                        approval = True
                    else:
                        corrected_interest_rate = 16
                else:
                    approval = False

            monthly_installment = (loan_amount * (1 + corrected_interest_rate / 100)) / tenure

            return Response({
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest_rate,
                "tenure": tenure,
                "monthly_installment": round(monthly_installment, 2)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateLoanView(APIView):
    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            customer_id = data["customer_id"]
            loan_amount = data["loan_amount"]
            interest_rate = data["interest_rate"]
            tenure = data["tenure"]

            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

            # Fetch all previous loans
            loans = customer.loans.all()

            current_year = date.today().year
            total_loans = loans.count()
            total_paid_on_time = sum(l.emis_paid_on_time for l in loans)
            current_year_loans = loans.filter(start_date__year=current_year).count()
            approved_volume = sum(l.loan_amount for l in loans)
            total_emi = sum(l.monthly_repayment for l in loans)
            current_total_debt = sum(l.loan_amount for l in loans)

            if current_total_debt > customer.approved_limit:
                credit_score = 0
            else:
                credit_score = 100
                credit_score -= (total_loans * 5)
                credit_score += total_paid_on_time * 0.5
                credit_score += current_year_loans * 2
                credit_score -= (approved_volume / 1000000)
                credit_score = max(0, min(credit_score, 100))

            approval = False
            corrected_interest_rate = interest_rate
            message = "Loan Approved"

            if total_emi + (loan_amount / tenure) > 0.5 * customer.monthly_income:
                approval = False
                message = "Rejected: EMI exceeds 50% of income"
            else:
                if credit_score > 50:
                    approval = True
                elif 30 < credit_score <= 50:
                    if interest_rate >= 12:
                        approval = True
                    else:
                        corrected_interest_rate = 12
                        approval = True
                elif 10 < credit_score <= 30:
                    if interest_rate >= 16:
                        approval = True
                    else:
                        corrected_interest_rate = 16
                        approval = True
                else:
                    approval = False
                    message = "Rejected: Credit score too low"

            monthly_installment = (loan_amount * (1 + corrected_interest_rate / 100)) / tenure

            if approval:
                loan_id = uuid.uuid4().hex[:10].upper()
                today = date.today()
                end_date = today + timedelta(days=30*tenure)

                Loan.objects.create(
                    customer=customer,
                    loan_id=loan_id,
                    loan_amount=loan_amount,
                    tenure=tenure,
                    interest_rate=corrected_interest_rate,
                    monthly_repayment=round(monthly_installment, 2),
                    emis_paid_on_time=0,
                    start_date=today,
                    end_date=end_date
                )

                return Response({
                    "loan_id": loan_id,
                    "customer_id": customer_id,
                    "loan_approved": True,
                    "message": "Loan Approved",
                    "monthly_installment": round(monthly_installment, 2)
                })

            return Response({
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": message,
                "monthly_installment": round(monthly_installment, 2)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewLoanDetail(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LoanDetailSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        loans = Loan.objects.filter(customer=customer)
        serializer = CustomerLoanListSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
