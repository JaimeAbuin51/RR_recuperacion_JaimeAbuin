# Aplicación de Recetas - Django

## Instalación

### Requisitos
- Python 3.10+
- pip
- Git

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repo-url>
cd rrecipes
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install django==4.2
pip install django-crispy-forms
pip install crispy-bootstrap4
pip install pillow
pip install python-decouple
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Iniciar servidor**
```bash
python manage.py runserver
```

Accede a http://127.0.0.1:8000/recetas/

## Funcionalidades

- Listar, crear, editar y eliminar recetas
- Sistema de comentarios
- Búsqueda y filtrado por categoría
- Autenticación de usuarios
- Panel de administración

## Tecnologías

- Django 4.2
- SQLite
- Bootstrap 5
- Crispy Forms