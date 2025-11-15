from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """커스텀 유저 모델"""
    phone = models.CharField('전화번호', max_length=20, blank=True)
    is_suspended = models.BooleanField('계정 정지', default=False)
    suspended_until = models.DateTimeField('정지 종료일', null=True, blank=True)
    created_at = models.DateTimeField('가입일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    """사용자 프로필 및 신용도"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    reputation_score = models.IntegerField('신용도 점수', default=100)
    level = models.IntegerField('레벨', default=1)
    
    # 통계
    total_auctions_created = models.IntegerField('총 개설 경매 수', default=0)
    total_bids_made = models.IntegerField('총 입찰 횟수', default=0)
    total_wins = models.IntegerField('총 낙찰 횟수', default=0)
    total_sales = models.IntegerField('총 판매 횟수', default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'profiles'
        verbose_name = '프로필'
        verbose_name_plural = '프로필 목록'
    
    def __str__(self):
        return f'{self.user.username}의 프로필'