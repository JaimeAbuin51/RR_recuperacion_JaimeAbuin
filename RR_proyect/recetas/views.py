from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Receta, Comentario
from .forms import RecetaForm, ComentarioForm

class ListaRecetas(ListView):
    model = Receta
    template_name = 'recetas/lista_recetas.html'
    context_object_name = 'recetas'
    paginate_by = 10

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
        return super().form_valid(form)