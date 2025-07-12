from django.contrib import admin
from django.utils.html import format_html
from .models import Jogador, Dupla, Partida
from .utils import ranking_individual, ranking_duplas


@admin.action(description='Gerar ranking individual no terminal')
def gerar_ranking_individual(modeladmin, request, queryset):
    """Action para gerar ranking individual no terminal."""
    ranking = ranking_individual()
    for pos, item in enumerate(ranking, start=1):
        print(f"{pos}. {item['jogador']} - "
              f"Vitórias: {item['vitorias']}, "
              f"Média: {item['media_pontos']:.2f}, "
              f"Eficiência: {item['eficiencia']:.2f}%")


@admin.action(description='Gerar ranking de duplas no terminal')
def gerar_ranking_duplas(modeladmin, request, queryset):
    """Action para gerar ranking de duplas no terminal."""
    ranking = ranking_duplas()
    for pos, item in enumerate(ranking, start=1):
        print(f"{pos}. {item['dupla']} - "
              f"Vitórias: {item['vitorias']}, "
              f"Partidas: {item['partidas']}")


@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'total_partidas', 'total_vitorias')
    search_fields = ('nome',)
    
    def total_partidas(self, obj):
        """Retorna o total de partidas do jogador."""
        from django.db.models import Q
        return Partida.objects.filter(
            Q(dupla1__jogadores=obj) | Q(dupla2__jogadores=obj)
        ).count()
    total_partidas.short_description = 'Total de Partidas'
    
    def total_vitorias(self, obj):
        """Retorna o total de vitórias do jogador."""
        from django.db.models import Q
        vitorias = 0
        partidas = Partida.objects.filter(
            Q(dupla1__jogadores=obj) | Q(dupla2__jogadores=obj)
        )
        for partida in partidas:
            if obj in partida.dupla1.jogadores.all():
                if partida.pontos_dupla1 > partida.pontos_dupla2:
                    vitorias += 1
            else:
                if partida.pontos_dupla2 > partida.pontos_dupla1:
                    vitorias += 1
        return vitorias
    total_vitorias.short_description = 'Total de Vitórias'


@admin.register(Dupla)
class DuplaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'jogadores_lista', 'total_partidas_dupla')
    filter_horizontal = ('jogadores',)
    
    def jogadores_lista(self, obj):
        """Retorna a lista de jogadores da dupla."""
        return ", ".join([j.nome for j in obj.jogadores.all()])
    jogadores_lista.short_description = 'Jogadores'
    
    def total_partidas_dupla(self, obj):
        """Retorna o total de partidas da dupla."""
        from django.db.models import Q
        return Partida.objects.filter(
            Q(dupla1=obj) | Q(dupla2=obj)
        ).count()
    total_partidas_dupla.short_description = 'Total de Partidas'


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('data', 'dupla1', 'pontos_dupla1', 'dupla2',
                    'pontos_dupla2', 'vencedor_display', 'capotinho_display')
    list_filter = ('data', 'dupla1__jogadores', 'dupla2__jogadores')
    date_hierarchy = 'data'
    actions = [gerar_ranking_individual, gerar_ranking_duplas]
    
    def vencedor_display(self, obj):
        """Exibe o vencedor da partida com destaque."""
        vencedor = obj.vencedor()
        return format_html(
            '<strong style="color: green;">{}</strong>',
            vencedor
        )
    vencedor_display.short_description = 'Vencedor'
    
    def capotinho_display(self, obj):
        """Exibe se houve capotinho."""
        if obj.tem_capotinho():
            dupla_capotinho = obj.dupla_capotinho()
            return format_html(
                '<strong style="color: red;">CAPOTINHO: {}</strong>',
                dupla_capotinho
            )
        return "—"
    capotinho_display.short_description = 'Capotinho'
    
    def get_queryset(self, request):
        """Otimiza queries para o admin."""
        return super().get_queryset(request).select_related(
            'dupla1', 'dupla2'
        ).prefetch_related(
            'dupla1__jogadores', 'dupla2__jogadores'
        )
