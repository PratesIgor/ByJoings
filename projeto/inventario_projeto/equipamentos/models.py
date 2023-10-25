from django.db import models

class Equipamento(models.Model):
    id = models.AutoField(primary_key=True)
    equipamento = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    serial = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    nome_responsavel = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add=True)
    terminal = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)

    def __str__(self):
        return self.equipamento

