from django.contrib import admin
from .models import Problem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
	list_display = ('title', 'difficulty', 'solved')
	list_filter = ('difficulty', 'solved')
	search_fields = ('title', 'description')
