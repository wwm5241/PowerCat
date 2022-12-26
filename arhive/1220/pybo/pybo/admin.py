from django.contrib import admin
from .models import Question
from .models import Answer

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    # 상속에 따른 속성 오버라이딩
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)