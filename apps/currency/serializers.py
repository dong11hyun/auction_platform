from rest_framework import serializers
from .models import Currency, CurrencyTransaction
from django.contrib.auth import get_user_model

User = get_user_model()


class CurrencySerializer(serializers.ModelSerializer):
    """재화 조회용 Serializer"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    total_balance = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Currency
        fields = [
            'id',
            'user',
            'username',
            'balance',
            'locked_balance',
            'total_balance',
            'total_earned',
            'total_spent',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'balance',
            'locked_balance',
            'total_earned',
            'total_spent',
            'created_at',
            'updated_at'
        ]


class CurrencyTransactionSerializer(serializers.ModelSerializer):
    """재화 거래 내역 조회용 Serializer"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    transaction_type_display = serializers.CharField(
        source='get_transaction_type_display',
        read_only=True
    )
    is_debit = serializers.BooleanField(read_only=True)
    is_credit = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CurrencyTransaction
        fields = [
            'id',
            'user',
            'username',
            'amount',
            'transaction_type',
            'transaction_type_display',
            'balance_before',
            'balance_after',
            'locked_balance_before',
            'locked_balance_after',
            'description',
            'reference_id',
            'is_debit',
            'is_credit',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'username',
            'amount',
            'transaction_type',
            'transaction_type_display',
            'balance_before',
            'balance_after',
            'locked_balance_before',
            'locked_balance_after',
            'description',
            'reference_id',
            'is_debit',
            'is_credit',
            'created_at'
        ]


class CurrencyTransactionCreateSerializer(serializers.Serializer):
    """재화 충전용 Serializer (Admin/테스트용)"""
    
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=1
    )
    description = serializers.CharField(
        max_length=500,
        required=False,
        default='수동 충전'
    )
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("충전 금액은 0보다 커야 합니다.")
        return value