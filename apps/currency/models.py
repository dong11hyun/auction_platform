from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Currency(models.Model):
    """사용자의 재화 보유 현황"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='currency',
        verbose_name='사용자'
    )
    
    # 재화 잔액
    balance = models.DecimalField(
        '사용 가능 재화',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    locked_balance = models.DecimalField(
        '잠금 재화',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='입찰 중이거나 사용 대기 중인 재화'
    )
    
    # 통계 (누적)
    total_earned = models.DecimalField(
        '총 획득 재화',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    total_spent = models.DecimalField(
        '총 사용 재화',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # 타임스탬프
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    
    class Meta:
        db_table = 'currencies'
        verbose_name = '재화'
        verbose_name_plural = '재화 목록'
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f'{self.user.username}의 재화 (잔액: {self.balance})'
    
    @property
    def total_balance(self):
        """총 재화 (사용 가능 + 잠금)"""
        return self.balance + self.locked_balance
    
    def can_spend(self, amount):
        """특정 금액을 사용할 수 있는지 확인"""
        return self.balance >= amount


class CurrencyTransaction(models.Model):
    """재화 거래 내역"""
    
    TRANSACTION_TYPES = [
        ('EARN', '획득'),
        ('CHARGE', '충전'),
        ('BID', '입찰'),
        ('BID_CANCEL', '입찰 취소'),
        ('WIN', '낙찰'),
        ('LOSE', '낙찰 실패'),
        ('REFUND', '환불'),
        ('FEE', '수수료'),
        ('RECEIVE', '판매 대금 수령'),
        ('LOCK', '재화 잠금'),
        ('UNLOCK', '재화 잠금 해제'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='currency_transactions',
        verbose_name='사용자'
    )
    
    amount = models.DecimalField(
        '금액',
        max_digits=15,
        decimal_places=2,
        help_text='양수: 증가, 음수: 감소'
    )
    
    transaction_type = models.CharField(
        '거래 유형',
        max_length=20,
        choices=TRANSACTION_TYPES
    )
    
    balance_before = models.DecimalField(
        '거래 전 잔액',
        max_digits=15,
        decimal_places=2
    )
    
    balance_after = models.DecimalField(
        '거래 후 잔액',
        max_digits=15,
        decimal_places=2
    )
    
    locked_balance_before = models.DecimalField(
        '거래 전 잠금 재화',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    locked_balance_after = models.DecimalField(
        '거래 후 잠금 재화',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # 관련 정보
    description = models.TextField('설명', blank=True)
    reference_id = models.CharField(
        '참조 ID',
        max_length=100,
        blank=True,
        help_text='관련 경매 ID, 주문 ID 등'
    )
    
    # 메타 정보
    ip_address = models.GenericIPAddressField('IP 주소', null=True, blank=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    
    class Meta:
        db_table = 'currency_transactions'
        verbose_name = '재화 거래 내역'
        verbose_name_plural = '재화 거래 내역 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['reference_id']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.get_transaction_type_display()} {self.amount}'
    
    @property
    def is_debit(self):
        """차감 거래인지 확인"""
        return self.amount < 0
    
    @property
    def is_credit(self):
        """적립 거래인지 확인"""
        return self.amount > 0