from django.db import models
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django

class Projeto(models.Model):
    nome_projeto = models.CharField(
        max_length=255, 
        verbose_name="Nome do Projeto"
    )

    descricao = models.TextField(
        blank=True,    
        null=True,     
        verbose_name="Descrição"
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projetos_criados' 
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ['-data_criacao'] 

    def __str__(self):
        """Retorna uma representação em string do objeto (útil no admin)."""
        return self.nome_projeto