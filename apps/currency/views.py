from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from decimal import Decimal
from django.utils import timezone

from .models import Currency, CurrencyTransaction
from .serializers import (
    CurrencySerializer,
    CurrencyTransactionSerializer,
    CurrencyTransactionCreateSerializer
)


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    재화 관리 ViewSet
    
    - GET /api/currency/ : 내 재화 조회
    - GET /api/currency/transactions/ : 거래 내역 조회
    - POST /api/currency/charge/ : 재화 충전 (테스트용)
    """
    
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """현재 사용자의 재화만 조회"""
        return Currency.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """
        보유 재화 조회
        GET /api/currency/
        """
        try:
            currency = Currency.objects.get(user=request.user)
            serializer = self.get_serializer(currency)
            return Response(serializer.data)
        except Currency.DoesNotExist:
            # Currency가 없으면 자동 생성
            currency = Currency.objects.create(user=request.user)
            serializer = self.get_serializer(currency)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['GET'])
    def transactions(self, request):
        """
        재화 거래 내역 조회
        GET /api/currency/transactions/
        
        Query Parameters:
        - type: 거래 유형 필터 (EARN, BID, REFUND 등)
        - start_date: 시작 날짜
        - end_date: 종료 날짜
        """
        queryset = CurrencyTransaction.objects.filter(user=request.user)
        
        # 거래 유형 필터
        transaction_type = request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # 날짜 필터
        start_date = request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        
        end_date = request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # 페이지네이션
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CurrencyTransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CurrencyTransactionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def charge(self, request):
        """
        재화 충전 (테스트/관리자용)
        POST /api/currency/charge/
        
        Body:
        {
            "amount": 10000,
            "description": "테스트 충전"
        }
        """
        serializer = CurrencyTransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get('description', '수동 충전')
        
        try:
            with transaction.atomic():
                # Currency 조회 (없으면 생성)
                currency, created = Currency.objects.get_or_create(
                    user=request.user
                )
                
                # 이전 잔액 저장
                balance_before = currency.balance
                locked_before = currency.locked_balance
                
                # 재화 증가
                currency.balance += amount
                currency.total_earned += amount
                currency.save()
                
                # 거래 내역 생성
                tx = CurrencyTransaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type='CHARGE',
                    balance_before=balance_before,
                    balance_after=currency.balance,
                    locked_balance_before=locked_before,
                    locked_balance_after=currency.locked_balance,
                    description=description,
                    ip_address=self.get_client_ip(request)
                )
                
                return Response({
                    'message': '재화 충전 성공',
                    'currency': CurrencySerializer(currency).data,
                    'transaction': CurrencyTransactionSerializer(tx).data
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """클라이언트 IP 주소 추출"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip