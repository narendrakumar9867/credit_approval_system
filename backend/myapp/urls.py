from django.urls import path
from .views import RegisterCustomerView, CheckEligibilityView, CreateLoanView, ViewLoanDetail, ViewLoansByCustomer

urlpatterns = [
    path('register', RegisterCustomerView.as_view(), name='register'),
    path('check-eligibility', CheckEligibilityView.as_view(), name='check-eligibility'),
    path('create-loan', CreateLoanView.as_view(), name='create-loan'),
    path('view-loan/<str:loan_id>', ViewLoanDetail.as_view(), name='view-loan'),
    path("view-loans/<int:customer_id>", ViewLoansByCustomer.as_view(), name="view-loans-by-customer"),
]
