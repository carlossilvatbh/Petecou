#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Criar superuser automaticamente se não existir
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@petecou.com', 'petecou2025!')
    print('Superuser admin criado com sucesso!')
else:
    print('Superuser admin já existe.')
"

# Criar dados de exemplo se não existirem partidas
python manage.py shell -c "
from jogos.models import Partida
if not Partida.objects.exists():
    import os
    os.system('python manage.py criar_dados_exemplo')
    print('Dados de exemplo criados!')
else:
    print('Dados já existem, pulando criação de exemplo.')
"
