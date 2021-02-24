# PARA REGISTRAR TODOS LOS MODELOS
# import django.apps
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):

    fieldsets = [("Encuestas", {"fields": ["question_text"]}), ("Información de la fecha", {"fields": ["pub_date"]})]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    search_fields = ["question_text"]


admin.site.index_title = "Inicio"
admin.site.site_header = "Polls Admin"
admin.site.site_title = "Polls Admin"
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

# models = django.apps.apps.get_models()
# print(models)

# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
