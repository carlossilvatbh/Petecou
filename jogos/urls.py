from django.urls import path
from . import views

app_name = 'jogos'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('ranking/individual/', views.ranking_individual_view,
         name='ranking_individual'),
    path('ranking/duplas/', views.ranking_duplas_view,
         name='ranking_duplas'),
    path('lancar-resultado/', views.lancar_resultado_view,
         name='lancar_resultado'),
    path('health/', views.health_check, name='health_check'),
]
