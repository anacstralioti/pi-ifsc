from django.db import models
from django.contrib.auth.models import (
    User,
) 


class Projeto(models.Model):
    nome_projeto = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Nome do Projeto"
    )

    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projetos_criados"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ["-data_criacao"]

    def __str__(self):
        """Retorna uma representação em string do objeto (útil no admin)."""
        return self.nome_projeto


class Tarefa(models.Model):
    nome_tarefa = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    categoria = models.CharField(
        max_length=30,
        choices=[
            ("URGENTE E IMPORTANTE","Urgente e Importante"),
            ("URGENTE NÃO IMPORTANTE", "Urgente não importante"),
            ("IMPORTANTE NÃO URGENTE", "Importante não Urgente"),
            ("IMPORTANTE E URGENTE", "Importante e Urgente"),
        ],
    )
    estimativa_horas = models.TimeField(null=False, blank=False)
    projeto = models.ForeignKey(
        "Projeto", on_delete=models.CASCADE, related_name="tarefas"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tarefas_atribuidas",
    )

    def __str__(self):
        return f"{self.nome_tarefa}"


class Apontamento(models.Model):
    hora_inicial = models.TimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )
    hora_final = models.TimeField(
        null=True,
    )
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    tarefa = models.ForeignKey(
        "Tarefa", on_delete=models.CASCADE, related_name="apontamentos"
    )

    def __str__(self):
        return f"Apontamento {self.id} - {self.descricao or 'Sem descrição'}"