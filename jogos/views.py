from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from .utils import ranking_individual, ranking_duplas, filtrar_por_periodo
from .models import Dupla, Partida


def ranking_individual_view(request):
    """View para exibir o ranking individual com filtros."""
    ano = timezone.now().year
    trimestre = request.GET.get('trimestre')
    partidas_minimas = int(request.GET.get('min_partidas', 3))
    
    # Filtra partidas por período
    partidas = filtrar_por_periodo(ano=ano, trimestre=trimestre)
    
    # Calcula ranking
    ranking = ranking_individual(partidas)
    
    # Filtra por número mínimo de partidas
    ranking = [j for j in ranking if j['partidas'] >= partidas_minimas]
    
    context = {
        'ranking': ranking,
        'ano': ano,
        'trimestre': trimestre,
        'partidas_minimas': partidas_minimas,
        'trimestres': [
            {'valor': '1', 'nome': '1º Trimestre'},
            {'valor': '2', 'nome': '2º Trimestre'},
            {'valor': '3', 'nome': '3º Trimestre'},
            {'valor': '4', 'nome': '4º Trimestre'},
        ]
    }
    
    return render(request, 'jogos/ranking_individual.html', context)


def ranking_duplas_view(request):
    """View para exibir o ranking de duplas com filtros."""
    ano = timezone.now().year
    trimestre = request.GET.get('trimestre')
    partidas_minimas = int(request.GET.get('min_partidas', 2))
    
    # Filtra partidas por período
    partidas = filtrar_por_periodo(ano=ano, trimestre=trimestre)
    
    # Calcula ranking
    ranking = ranking_duplas(partidas)
    
    # Filtra por número mínimo de partidas
    ranking = [d for d in ranking if d['partidas'] >= partidas_minimas]
    
    context = {
        'ranking': ranking,
        'ano': ano,
        'trimestre': trimestre,
        'partidas_minimas': partidas_minimas,
        'trimestres': [
            {'valor': '1', 'nome': '1º Trimestre'},
            {'valor': '2', 'nome': '2º Trimestre'},
            {'valor': '3', 'nome': '3º Trimestre'},
            {'valor': '4', 'nome': '4º Trimestre'},
        ]
    }
    
    return render(request, 'jogos/ranking_duplas.html', context)


def home_view(request):
    """View para a página inicial."""
    return render(request, 'jogos/home.html')


def lancar_resultado_view(request):
    """View para jogadores lançarem resultados de partidas."""
    duplas = Dupla.objects.all()
    
    if request.method == 'POST':
        try:
            dupla1_id = request.POST.get('dupla1')
            dupla2_id = request.POST.get('dupla2')
            pontos_dupla1 = int(request.POST.get('pontos_dupla1'))
            pontos_dupla2 = int(request.POST.get('pontos_dupla2'))
            data = request.POST.get('data')
            
            if dupla1_id == dupla2_id:
                messages.error(request,
                               'Uma dupla não pode jogar contra si mesma!')
                return render(request, 'jogos/lancar_resultado.html',
                              {'duplas': duplas})
            
            dupla1 = Dupla.objects.get(id=dupla1_id)
            dupla2 = Dupla.objects.get(id=dupla2_id)
            
            partida = Partida(
                dupla1=dupla1,
                dupla2=dupla2,
                pontos_dupla1=pontos_dupla1,
                pontos_dupla2=pontos_dupla2,
                data=data if data else timezone.now().date()
            )
            
            partida.clean()  # Valida as regras
            partida.save()
            
            # Mensagem de sucesso com informação sobre capotinho
            vencedor = partida.vencedor()
            msg = (f'Partida registrada: {partida.dupla1} '
                   f'{partida.pontos_dupla1} x {partida.pontos_dupla2} '
                   f'{partida.dupla2}. Vencedor: {vencedor}')
            
            if partida.tem_capotinho():
                msg += f' - CAPOTINHO para {partida.dupla_capotinho()}!'
            
            messages.success(request, msg)
            return redirect('jogos:lancar_resultado')
            
        except ValidationError as e:
            messages.error(request, f'Erro na validação: {e.message}')
        except Exception as e:
            messages.error(request, f'Erro ao registrar partida: {str(e)}')
    
    context = {
        'duplas': duplas,
        'hoje': timezone.now().date()
    }
    
    return render(request, 'jogos/lancar_resultado.html', context)
