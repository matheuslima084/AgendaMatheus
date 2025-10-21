from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=20)
    sobrenome = models.CharField(max_length=20)
    descricao = models.TextField(max_length=255)
    telefone = models.CharField(max_length=20)  # Melhor usar CharField para telefone
    imagem = models.ImageField(upload_to='core_imagens/%Y/%m/', blank=True, null=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
