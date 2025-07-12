from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random
from jogos.models import Jogador, Dupla, Partida


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de exemplo...')

        # Criar jogadores
        jogadores_nomes = [
            'José Pinheiro', 'Rodrigo', 'Lucas', 'André Baeta',
            'Pedro', 'André Lara', 'Theo', 'Marcelinho',
            'Diogo', 'Cássio', 'Fernandão', 'Cajuzinho'
        ]

        jogadores = []
        for nome in jogadores_nomes:
            jogador, created = Jogador.objects.get_or_create(nome=nome)
            if created:
                self.stdout.write(f'  Criado jogador: {nome}')
            jogadores.append(jogador)

        # Criar duplas (diferentes combinações)
        duplas = []
        import itertools
        combinacoes = list(itertools.combinations(jogadores, 2))
        
        # Criar algumas duplas aleatórias
        max_duplas = min(10, len(combinacoes))
        duplas_selecionadas = random.sample(combinacoes, max_duplas)
        
        for jog1, jog2 in duplas_selecionadas:
            dupla = Dupla.objects.create()
            dupla.jogadores.set([jog1, jog2])
            dupla.save()
            self.stdout.write(f'  Criada dupla: {dupla}')
            duplas.append(dupla)

        # Criar partidas dos últimos 6 meses
        self.stdout.write('Criando partidas...')
        inicio = date.today() - timedelta(days=180)
        
        for i in range(50):  # Criar 50 partidas
            data_partida = inicio + timedelta(days=random.randint(0, 180))
            dupla1, dupla2 = random.sample(duplas, 2)
            
            # Gerar pontuações seguindo as novas regras (máximo 20)
            # 70% das partidas terminam em 20 pontos
            if random.random() < 0.7:
                # Uma dupla chega a 20
                pontos_vencedor = 20
                # Perdedor pode fazer entre 8 e 19 pontos
                pontos_perdedor = random.randint(8, 19)
                # 20% chance de capotinho (perdedor ≤ 10)
                if random.random() < 0.2:
                    pontos_perdedor = random.randint(5, 10)
            else:
                # Jogo termina antes dos 20 com diferença mínima de 2
                pontos_base = random.randint(15, 19)
                diferenca = random.randint(2, 5)
                pontos_vencedor = pontos_base
                pontos_perdedor = pontos_base - diferenca
                # Garantir que não seja negativo
                if pontos_perdedor < 0:
                    pontos_perdedor = 0
            
            # Decidir qual dupla vence aleatoriamente
            if random.random() < 0.5:
                pontos_dupla1 = pontos_vencedor
                pontos_dupla2 = pontos_perdedor
            else:
                pontos_dupla1 = pontos_perdedor
                pontos_dupla2 = pontos_vencedor

            partida, created = Partida.objects.get_or_create(
                data=data_partida,
                dupla1=dupla1,
                dupla2=dupla2,
                defaults={
                    'pontos_dupla1': pontos_dupla1,
                    'pontos_dupla2': pontos_dupla2,
                }
            )
            
            if created:
                capotinho_info = ""
                if partida.tem_capotinho():
                    capotinho_info = " (CAPOTINHO!)"
                
                self.stdout.write(
                    f'  Partida: {dupla1} {pontos_dupla1} x '
                    f'{pontos_dupla2} {dupla2}{capotinho_info}'
                )

        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo criados com sucesso!')
        )
        self.stdout.write(
            f'Total: {Jogador.objects.count()} jogadores, '
            f'{Dupla.objects.count()} duplas, '
            f'{Partida.objects.count()} partidas'
        )
