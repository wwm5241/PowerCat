from django.apps import AppConfig

# pybo 하위의 db.sqlite3와 연동
class PyboConfig(AppConfig):
    # pybo안의 데이터베이스 필드 연동
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'
