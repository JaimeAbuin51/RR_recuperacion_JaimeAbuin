from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Receta, Comentario, Categoria
from .forms import RecetaForm, ComentarioForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import requests

class ListaRecetas(ListView):
    model = Receta
    template_name = 'recetas/lista_recetas.html'
    context_object_name = 'recetas'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        categoria = self.request.GET.get('categoria')
        
        if search:
            queryset = queryset.filter(titulo__icontains=search)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['categorias'] = Categoria.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')
        return context

class DetalleReceta(DetailView):
    model = Receta
    template_name = 'recetas/detalle_receta.html'
    context_object_name = 'receta'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = Comentario.objects.filter(receta=self.object)
        context['form'] = ComentarioForm()
        return context

class CrearReceta(LoginRequiredMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/crear_receta.html'
    success_url = reverse_lazy('lista_recetas')
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, 'Receta creada exitosamente', extra_tags='success')
        return super().form_valid(form)

class EditarReceta(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/editar_receta.html'
    
    def test_func(self):
        receta = self.get_object()
        return self.request.user == receta.autor
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para editar esta receta')
        return redirect('lista_recetas')
    
    def form_valid(self, form):
        messages.success(self.request, 'Receta actualizada exitosamente', extra_tags='success')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detalle_receta', kwargs={'pk': self.object.pk})

class EliminarReceta(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Receta
    template_name = 'recetas/eliminar_receta.html'
    success_url = reverse_lazy('lista_recetas')
    
    def test_func(self):
        receta = self.get_object()
        return self.request.user == receta.autor
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para eliminar esta receta')
        return redirect('lista_recetas')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Receta eliminada exitosamente', extra_tags='success')
        return super().delete(request, *args, **kwargs)

@login_required
def crear_comentario(request, receta_id):
    receta = get_object_or_404(Receta, pk=receta_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.receta = receta
            comentario.save()
            return redirect('detalle_receta', pk=receta.pk)
    return redirect('detalle_receta', pk=receta.pk)

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    if request.user == comentario.autor:
        receta_id = comentario.receta.id
        comentario.delete()
        return redirect('detalle_receta', pk=receta_id)
    return redirect('lista_recetas')

class CustomLoginView(LoginView):
    template_name = 'recetas/login.html'
    
class CustomLogoutView(LogoutView):
    pass

class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = 'recetas/registro.html'
    success_url = reverse_lazy('login')

class BuscarRecetasExternas(ListView):
    template_name = 'recetas/buscar_externas.html'
    context_object_name = 'recetas_externas'
    paginate_by = 10
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        if not search:
            return []
        
        try:
            url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={search}'
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get('meals'):
                return data['meals']
            return []
        except:
            return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['categorias'] = Categoria.objects.all()
        return context

def detalle_externa(request, meal_id):
    try:
        url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get('meals'):
            receta = data['meals'][0]
            categorias = Categoria.objects.all()
            return render(request, 'recetas/detalle_externa.html', {'receta': receta, 'categorias': categorias})
    except:
        pass
    
    return redirect('buscar_externas')

@login_required
def guardar_externa(request):
    if request.method == 'POST':
        titulo = request.POST.get('meal_name')
        categoria_id = request.POST.get('categoria')
        instrucciones = request.POST.get('meal_instructions')
        imagen_url = request.POST.get('meal_image')
        
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            receta = Receta.objects.create(
                titulo=titulo,
                ingredientes='Receta importada de TheMealDB',
                pasos=instrucciones,
                tiempo_preparacion=30,
                categoria=categoria,
                autor=request.user
            )
            messages.success(request, 'Receta guardada exitosamente', extra_tags='success')
            return redirect('detalle_receta', pk=receta.pk)
        except:
            messages.error(request, 'Error al guardar la receta')
            return redirect('buscar_externas')
    
    return redirect('buscar_externas')