from django.contrib import admin
# from django.contrib.admin.actions import delete_selected as original_delete_selected
from .models import TestModel, Question, Choice, UserChoice, OngoingTests, UserTest, UserAnswer
import os
from django.conf import settings
def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        file_path = os.path.join(settings.BASE_DIR, 'tests')
        file_path = os.path.join(file_path, str(obj.uid)+'.json')
        os.remove(file_path)
        obj.delete()  # This calls the custom delete method
    # original_delete_selected(modeladmin, request, queryset)

# admin.site.add_action(delete_selected, 'delete_selected')

class OptionInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

class QuizAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)
    # fields = ['user','name']
    # search_fields = ['name','count']
    list_display = ['name','uid','created_at','count']
    actions = [delete_model]
class OngoingTestsAdmin(admin.ModelAdmin):
    list_display = ['user','quiz']

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user','quiz']
    list_filter = ['user','quiz']
    filter_horizontal = ('choices',)
    search_fields = ['user__username','quiz__name']
class UserTestAdmin(admin.ModelAdmin):
    list_display = ['user','quiz','correct','incorrect','total','started_time','ended_time']
    list_filter = ['user','quiz']
    search_fields = ['user__username','quiz__name']

    
admin.site.register(TestModel, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(OngoingTests, OngoingTestsAdmin)
admin.site.register(UserTest, UserTestAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
