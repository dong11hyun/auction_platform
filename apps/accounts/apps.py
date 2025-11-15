from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'  # ← 'accounts'가 아니라 'apps.accounts'
    verbose_name = '회원 관리'