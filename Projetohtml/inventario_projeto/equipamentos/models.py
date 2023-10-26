from django.db import models

class Equipamento(models.Model):
    id = models.AutoField(primary_key=True)
    equipamento = models.CharField(max_length=100, db_column='equipamento')
    valor = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor')
    serial = models.CharField(max_length=100, db_column='serial')
    departamento = models.CharField(max_length=100, db_column='departamento')
    nome_responsavel = models.CharField(max_length=100, db_column='nome_responsavel')
    telefone = models.CharField(max_length=15, db_column='telefone')
    email = models.EmailField(max_length=100, db_column='email')
    data_hora = models.DateTimeField(auto_now_add=True, db_column='data_hora')
    terminal = models.CharField(max_length=100, db_column='terminal')
    usuario = models.CharField(max_length=100, db_column='usuario')

    class Meta:
        managed = False  # Isso impede que o Django gere tabelas no banco de dados
        db_table = 'equipamentos_equipamento'  # Especifique o nome da tabela no banco

    def _str_(self):
        return self.equipamento

