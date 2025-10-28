from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Importe o timezone
from datetime import timedelta # Importe timedelta

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
    cancelado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ["-data_criacao"]

    def __str__(self):
        return self.nome_projeto


class Tarefa(models.Model):
    nome_tarefa = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    categoria = models.CharField(
        max_length=30,
        choices=[
            ("URGENTE_IMPORTANTE", "Importante e Urgente"),
            ("IMPORTANTE_NAO_URGENTE", "Importante e Não Urgente"),
            ("URGENTE_NAO_IMPORTANTE", "Urgente e Não Importante"),
            ("NAO_IMPORTANTE_NAO_URGENTE", "Não Importante e Não Urgente"),
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

    @property
    def total_horas_gastas_str(self):
        """Calcula o total de horas gastas a partir dos apontamentos."""
        total_duration = timedelta()
        apontamentos_concluidos = self.apontamentos.filter(
            hora_inicial__isnull=False, hora_final__isnull=False
        )
        
        for ap in apontamentos_concluidos:
            if ap.duracao:
                total_duration += ap.duracao
        
        total_seconds = int(total_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f'{hours:02}:{minutes:02}'
    
    @property
    def apontamento_ativo(self):
        """Retorna o apontamento ativo (sem hora_final), se existir."""
        return self.apontamentos.filter(hora_final__isnull=True).first()


class Apontamento(models.Model):
    hora_inicial = models.DateTimeField(
        null=False,
        blank=False,
    )
    hora_final = models.DateTimeField(
        null=True, 
        blank=True
    )
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    tarefa = models.ForeignKey(
        "Tarefa", on_delete=models.CASCADE, related_name="apontamentos"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apontamentos"
    )

    def __str__(self):
        return f"Apontamento {self.id} - {self.tarefa.nome_tarefa}"

    @property
    def duracao_formatada(self):
        """Retorna a duração formatada como HH:MM:SS."""
        d = self.duracao
        if d:
            total_seconds = int(d.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f'{hours:02}:{minutes:02}:{seconds:02}'
        return "00:00:00"
        
    @property
    def duracao(self):
        """Retorna a duração (timedelta) do apontamento se estiver concluído."""
        if self.hora_final and self.hora_inicial:
            return self.hora_final - self.hora_inicial
        return None