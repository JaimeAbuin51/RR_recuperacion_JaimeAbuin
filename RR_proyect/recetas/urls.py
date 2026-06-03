from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_recetas, name='lista_recetas'),
    path('receta/<int:pk>/', views.DetalleReceta.as_view(), name='detalle_receta'),
    path('crear/', views.CrearReceta.as_view(), name='crear_receta'),
    path('editar/<int:pk>/', views.EditarReceta.as_view(), name='editar_receta'),
    path('eliminar/<int:pk>/', views.EliminarReceta.as_view(), name='eliminar_receta'),
    path('comentario/crear/<int:receta_id>/', views.crear_comentario, name='crear_comentario'),
    path('comentario/eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(next_page='lista_recetas'), name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('externas/', views.BuscarRecetasExternas.as_view(), name='buscar_externas'),
    path('externas/<path:meal_id>/', views.detalle_externa, name='detalle_externa'),
    path('guardar-externa/', views.guardar_externa, name='guardar_externa'),
]