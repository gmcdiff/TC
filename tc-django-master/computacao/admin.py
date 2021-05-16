from django.contrib import admin

# Register your models here.
from .models import Automato,Maquina
admin.site.register(Automato)
admin.site.register(Maquina)