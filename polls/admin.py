from django.contrib import admin
from .models import *
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    # 추가옵션 개수
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문 섹션', {'fields': ['question_text']}),
        # 생성일 숨김(collapse)
        ('생성일', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # 보다 깔끔하게 질문과 날짜를 출력
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    # pub_date 필드를 수정 불가능하게 설정
    readonly_fields = ['pub_date']
    inlines = [ChoiceInline]
    # 생성일을 기준으로 필터 추가
    list_filter = ['pub_date']
    # Question과 Choice에 대한 검색 기능 추가
    search_fields = ['question_text', 'choice__choice_text']

admin.site.register(Question, QuestionAdmin)