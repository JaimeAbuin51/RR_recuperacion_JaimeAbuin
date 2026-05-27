from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaRecetas.as_view(), name='lista_recetas'),
    path('receta/<int:pk>/', views.DetalleReceta.as_view(), name='detalle_receta'),
    path('crear/', views.CrearReceta.as_view(), name='crear_receta'),
    path('editar/<int:pk>/', views.EditarReceta.as_view(), name='editar_receta'),
    path('eliminar/<int:pk>/', views.EliminarReceta.as_view(), name='eliminar_receta'),
    path('comentario/crear/<int:receta_id>/', views.crear_comentario, name='crear_comentario'),
    path('comentario/eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
]