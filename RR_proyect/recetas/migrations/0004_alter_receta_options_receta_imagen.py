from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0003_comentario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receta',
            options={'ordering': ['-fecha_creacion']},
        ),
        migrations.AddField(
            model_name='receta',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='recetas/'),
        ),
    ]
