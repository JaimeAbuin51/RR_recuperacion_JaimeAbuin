from django.contrib import admin
from .models import Categoria, Receta, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'fecha_creacion']
    list_filter = ['categoria', 'fecha_creacion']
    search_fields = ['titulo', 'autor__username']
    readonly_fields = ['fecha_creacion', 'autor']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'receta', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['autor__username', 'receta__titulo']
    readonly_fields = ['fecha_creacion', 'autor']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)