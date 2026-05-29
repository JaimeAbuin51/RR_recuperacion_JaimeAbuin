from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from .models import Receta, Comentario, Categoria
from .forms import RecetaForm, ComentarioForm

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

class CrearReceta(LoginRequiredMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/crear_receta.html'
    success_url = reverse_lazy('lista_recetas')
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, 'Receta creada exitosamente', extra_tags='success')
        return super().form_valid(form)
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EditarReceta(LoginRequiredMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/editar_receta.html'
    
    def get_success_url(self):
        return reverse_lazy('detalle_receta', kwargs={'pk': self.object.pk})
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para editar esta receta')
        return redirect('lista_recetas')
    
    def form_valid(self, form):
        messages.success(self.request, 'Receta actualizada exitosamente', extra_tags='success')
        return super().form_valid(form)

    def test_func(self):
        receta = self.get_object()
        return self.request.user == receta.autor

class EliminarReceta(LoginRequiredMixin, DeleteView):
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

class EditarReceta(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/editar_receta.html'
    
    def test_func(self):
        receta = self.get_object()
        return self.request.user == receta.autor
    
    def handle_no_permission(self):
        return redirect('lista_recetas')
    
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
        return redirect('lista_recetas')