from django.db import models
from django.contrib.auth.models import User

categorias = [
    (1, 'Junta Municipal de Agua y Saneamiento JMAS'),
    (2, 'Comision Federal de Electricidad CFE'),
    (3, 'Gas Natural'),
    (4, 'Direccion General de Desarrollo Urbano'),
    (5, 'Ecología y Protección Civil'),
    (6, 'Movilidad'),
    (7, 'Obras Públicas'),
    (8, 'Planeación del Desarrollo Municipal'),
    (9, 'Salud Pública'),
    (10, 'Otras')
]
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    startdate = models.DateTimeField(auto_now_add=True)
    completedate =models.DateTimeField(null=True, blank=True)
    category = models.IntegerField(null=False, blank=False,
        choices=categorias,
        default=1
    )
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owmer = models.IntegerField(blank=False, default=10)

    def __str__(self):
        return self.title +'- by ' + self.user.username


        



