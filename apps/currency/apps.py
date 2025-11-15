from django.apps import AppConfig


class CurrencyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.currency'  # ← 'currency'가 아니라 'apps.currency'
    verbose_name = '재화 관리'
    
    def ready(self):
        import apps.currency.signals  # Signal 등록