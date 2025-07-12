from django.db.models import Q
from .models import Jogador, Dupla, Partida


def ranking_individual(partidas_queryset=None):
    """
    Calcula o ranking individual dos jogadores.
    
    Args:
        partidas_queryset: QuerySet de partidas para filtrar (opcional)
    
    Returns:
        Lista de dicionários com estatísticas dos jogadores
    """
    if partidas_queryset is None:
        partidas_queryset = Partida.objects.all()
    
    jogadores = Jogador.objects.all()
    ranking = []
    
    for jogador in jogadores:
        partidas = partidas_queryset.filter(
            Q(dupla1__jogadores=jogador) | Q(dupla2__jogadores=jogador)
        )
        total_partidas = partidas.count()
        
        if total_partidas == 0:
            continue
            
        total_pontos = 0
        total_vitorias = 0
        capotinhos_dados = 0  # Capotinhos que o jogador deu
        capotinhos_tomados = 0  # Capotinhos que o jogador tomou
        
        for partida in partidas:
            if jogador in partida.dupla1.jogadores.all():
                pontos = partida.pontos_dupla1
                venceu = partida.pontos_dupla1 > partida.pontos_dupla2
                dupla_jogador = partida.dupla1
            else:
                pontos = partida.pontos_dupla2
                venceu = partida.pontos_dupla2 > partida.pontos_dupla1
                dupla_jogador = partida.dupla2
            
            total_pontos += pontos
            if venceu:
                total_vitorias += 1
                # Se venceu e adversário fez <= 10, deu capotinho
                if partida.tem_capotinho():
                    capotinhos_dados += 1
            else:
                # Se perdeu e fez <= 10, tomou capotinho
                if (partida.tem_capotinho() and
                        partida.dupla_capotinho() == dupla_jogador):
                    capotinhos_tomados += 1
        
        media_pontos = (total_pontos / total_partidas
                        if total_partidas > 0 else 0)
        eficiencia = ((total_vitorias / total_partidas) * 100
                      if total_partidas > 0 else 0)
        
        ranking.append({
            'jogador': jogador,
            'partidas': total_partidas,
            'pontos': total_pontos,
            'vitorias': total_vitorias,
            'media_pontos': media_pontos,
            'eficiencia': eficiencia,
            'capotinhos_dados': capotinhos_dados,
            'capotinhos_tomados': capotinhos_tomados,
        })
    
    # Ordena por eficiência e depois por média de pontos
    ranking.sort(key=lambda x: (x['eficiencia'], x['media_pontos']),
                 reverse=True)
    return ranking


def ranking_duplas(partidas_queryset=None):
    """
    Calcula o ranking das duplas.
    
    Args:
        partidas_queryset: QuerySet de partidas para filtrar (opcional)
    
    Returns:
        Lista de dicionários com estatísticas das duplas
    """
    if partidas_queryset is None:
        partidas_queryset = Partida.objects.all()
    
    duplas = Dupla.objects.all()
    ranking = []
    
    for dupla in duplas:
        partidas = partidas_queryset.filter(Q(dupla1=dupla) | Q(dupla2=dupla))
        total_partidas = partidas.count()
        
        if total_partidas == 0:
            continue
            
        total_vitorias = sum(1 for partida in partidas
                             if partida.vencedor() == dupla)
        eficiencia = ((total_vitorias / total_partidas) * 100
                      if total_partidas > 0 else 0)
        
        # Contabilizar capotinhos
        capotinhos_dados = sum(1 for partida in partidas
                               if (partida.vencedor() == dupla and
                                   partida.tem_capotinho()))
        capotinhos_tomados = sum(1 for partida in partidas
                                 if (partida.dupla_capotinho() == dupla))
        
        ranking.append({
            'dupla': dupla,
            'partidas': total_partidas,
            'vitorias': total_vitorias,
            'eficiencia': eficiencia,
            'capotinhos_dados': capotinhos_dados,
            'capotinhos_tomados': capotinhos_tomados,
        })
    
    # Ordena por número de vitórias e depois por eficiência
    ranking.sort(key=lambda x: (x['vitorias'], x['eficiencia']), reverse=True)
    return ranking


def filtrar_por_periodo(ano=2025, trimestre=None):
    """
    Filtra partidas por período (ano e trimestre opcional).
    
    Args:
        ano: Ano para filtrar
        trimestre: Trimestre (1, 2, 3, 4) - opcional
    
    Returns:
        QuerySet de partidas filtradas
    """
    partidas = Partida.objects.filter(data__year=ano)
    
    if trimestre:
        trimestres = {
            1: (1, 3),
            2: (4, 6),
            3: (7, 9),
            4: (10, 12)
        }
        
        if int(trimestre) in trimestres:
            inicio, fim = trimestres[int(trimestre)]
            partidas = partidas.filter(
                data__month__gte=inicio,
                data__month__lte=fim
            )
    
    return partidas
