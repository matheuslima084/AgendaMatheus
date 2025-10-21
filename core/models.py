from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=20)
    sobrenome = models.CharField(max_length=20)
    descricao = models.TextField(max_length=255)
    telefone = models.IntegerField()
    imagem = models.ImageField(upload_to='core_imagens/%Y/%m/', blank=True, null=True)
