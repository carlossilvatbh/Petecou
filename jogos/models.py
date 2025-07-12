from django.db import models
from django.utils import timezone


class Jogador(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"


class Dupla(models.Model):
    jogadores = models.ManyToManyField(Jogador)

    def __str__(self):
        return " & ".join([j.nome for j in self.jogadores.all()])

    class Meta:
        verbose_name = "Dupla"
        verbose_name_plural = "Duplas"


class Partida(models.Model):
    data = models.DateField(default=timezone.now)
    dupla1 = models.ForeignKey(
        Dupla, related_name='partidas_dupla1', on_delete=models.CASCADE
    )
    dupla2 = models.ForeignKey(
        Dupla, related_name='partidas_dupla2', on_delete=models.CASCADE
    )
    pontos_dupla1 = models.PositiveIntegerField()
    pontos_dupla2 = models.PositiveIntegerField()

    def __str__(self):
        capotinho_info = ""
        if self.tem_capotinho():
            if (self.pontos_dupla1 <= 10 and
                    self.pontos_dupla1 < self.pontos_dupla2):
                capotinho_info = " (Capotinho dupla1)"
            elif (self.pontos_dupla2 <= 10 and
                  self.pontos_dupla2 < self.pontos_dupla1):
                capotinho_info = " (Capotinho dupla2)"
        
        return (f"{self.dupla1} x {self.dupla2} "
                f"({self.pontos_dupla1} - {self.pontos_dupla2})"
                f"{capotinho_info}")

    def vencedor(self):
        if self.pontos_dupla1 > self.pontos_dupla2:
            return self.dupla1
        return self.dupla2

    def perdedor(self):
        if self.pontos_dupla1 < self.pontos_dupla2:
            return self.dupla1
        return self.dupla2

    def tem_capotinho(self):
        """Verifica se houve capotinho (perdedor fez 10 pontos ou menos)"""
        pontos_perdedor = min(self.pontos_dupla1, self.pontos_dupla2)
        return pontos_perdedor <= 10

    def dupla_capotinho(self):
        """Retorna a dupla que levou capotinho, se houver"""
        if self.tem_capotinho():
            return self.perdedor()
        return None

    def clean(self):
        """Validação personalizada"""
        from django.core.exceptions import ValidationError
        
        if self.pontos_dupla1 > 20:
            raise ValidationError('Pontos da dupla 1 não podem exceder 20.')
        if self.pontos_dupla2 > 20:
            raise ValidationError('Pontos da dupla 2 não podem exceder 20.')
        if self.pontos_dupla1 == self.pontos_dupla2:
            raise ValidationError('Não pode haver empate.')
        if max(self.pontos_dupla1, self.pontos_dupla2) < 20:
            if abs(self.pontos_dupla1 - self.pontos_dupla2) < 2:
                raise ValidationError(
                    'Jogo deve terminar em 20 pontos ou com '
                    'diferença mínima de 2 pontos.'
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"
        ordering = ['-data']
