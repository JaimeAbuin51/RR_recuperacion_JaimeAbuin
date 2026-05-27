from django.contrib import admin
from .models import Categoria, Receta, Comentario

admin.site.register(Categoria)
admin.site.register(Receta)
admin.site.register(Comentario)