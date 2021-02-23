from django.contrib import admin

from .models import Choice, Question


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]


admin.site.index_title = "Inicio"
admin.site.site_header = "Polls Admin"
admin.site.site_title = "Polls Admin"
admin.site.register(Question)
admin.site.register(Choice)
