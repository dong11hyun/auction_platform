from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Currency, CurrencyTransaction


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'balance_display',
        'locked_balance_display',
        'total_balance_display',
        'total_earned',
        'total_spent',
        'updated_at'
    ]
    
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_earned', 'total_spent', 'created_at', 'updated_at']
    
    fieldsets = (
        ('사용자 정보', {
            'fields': ('user',)
        }),
        ('재화 정보', {
            'fields': ('balance', 'locked_balance')
        }),
        ('통계', {
            'fields': ('total_earned', 'total_spent')
        }),
        ('타임스탬프', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def balance_display(self, obj):
        """잔액 표시 (색상 추가)"""
        color = 'green' if obj.balance > 0 else 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:,.0f}</span>',
            color,
            obj.balance
        )
    balance_display.short_description = '사용 가능 재화'
    
    def locked_balance_display(self, obj):
        """잠금 재화 표시"""
        if obj.locked_balance > 0:
            return format_html(
                '<span style="color: orange; font-weight: bold;">{:,.0f}</span>',
                obj.locked_balance
            )
        return '-'
    locked_balance_display.short_description = '잠금 재화'
    
    def total_balance_display(self, obj):
        """총 재화 표시"""
        return format_html(
            '<span style="font-weight: bold;">{:,.0f}</span>',
            obj.total_balance
        )
    total_balance_display.short_description = '총 재화'


@admin.register(CurrencyTransaction)
class CurrencyTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'transaction_type',
        'amount_display',
        'balance_after',
        'description_short',
        'created_at'
    ]
    
    list_filter = [
        'transaction_type',
        'created_at',
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'description',
        'reference_id'
    ]
    
    readonly_fields = [
        'user',
        'amount',
        'transaction_type',
        'balance_before',
        'balance_after',
        'locked_balance_before',
        'locked_balance_after',
        'description',
        'reference_id',
        'ip_address',
        'created_at'
    ]
    
    fieldsets = (
        ('거래 정보', {
            'fields': (
                'user',
                'transaction_type',
                'amount',
                'description',
                'reference_id'
            )
        }),
        ('잔액 정보', {
            'fields': (
                'balance_before',
                'balance_after',
                'locked_balance_before',
                'locked_balance_after'
            )
        }),
        ('기타', {
            'fields': ('ip_address', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Admin에서 직접 생성 불가"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Admin에서 삭제 불가 (감사 추적 보존)"""
        return False
    
    def amount_display(self, obj):
        """금액 표시 (색상 추가)"""
        if obj.amount > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">+{:,.0f}</span>',
                obj.amount
            )
        elif obj.amount < 0:
            return format_html(
                '<span style="color: red; font-weight: bold;">{:,.0f}</span>',
                obj.amount
            )
        return '0'
    amount_display.short_description = '금액'
    
    def description_short(self, obj):
        """설명 요약"""
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description
    description_short.short_description = '설명'