from rest_framework import serializers
from .models import Customer, Loan
from datetime import date

class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age', 'monthly_income', 'approved_limit', 'phone_number']
        read_only_fields = ['id', 'approved_limit']

    def create(self, validated_data):
        income = validated_data.get('monthly_income')
        approved_limit = round((36 * income) / 100000) * 100000 
        validated_data['approved_limit'] = approved_limit
        return super().create(validated_data)


class EligibilityCheckSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()
    

class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class LoanDetailSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "customer",
            "loan_amount",
            "interest_rate",
            "monthly_repayment",
            "tenure",
        ]

    def get_customer(self, obj):
        return {
            "id": obj.customer.id,
            "first_name": obj.customer.first_name,
            "last_name": obj.customer.last_name,
            "phone_number": obj.customer.phone_number,
            "age": obj.customer.age,
        }


class CustomerLoanListSerializer(serializers.ModelSerializer):
    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "loan_amount",
            "interest_rate",
            "monthly_repayment",
            "repayments_left",
        ]

    def get_repayments_left(self, obj):
        today = date.today()
        if obj.end_date < today:
            return 0
        months_left = (obj.end_date.year - today.year) * 12 + (obj.end_date.month - today.month)
        return max(0, months_left)
