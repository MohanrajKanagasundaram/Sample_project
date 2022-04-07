from django.contrib import admin
from procedure_app.models import Procedure,Section,Field

# Register your models here.
admin.site.register(Procedure)
admin.site.register(Section)
admin.site.register(Field)