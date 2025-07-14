#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting build process..."

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🔧 Collecting static files..."
python manage.py collectstatic --noinput

echo "🗄️ Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🔍 Debugging database..."
python manage.py debug_db

echo "👤 Creating superuser if needed..."
# Criar superuser automaticamente se não existir
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@petecou.com', 'petecou2025!')
    print('✅ Superuser admin criado com sucesso!')
else:
    print('ℹ️ Superuser admin já existe.')
"

echo "🎲 Creating sample data if needed..."
# Criar dados de exemplo se não existirem partidas
python manage.py shell -c "
from jogos.models import Partida
if not Partida.objects.exists():
    import os
    os.system('python manage.py criar_dados_exemplo')
    print('✅ Dados de exemplo criados!')
else:
    print('ℹ️ Dados já existem, pulando criação de exemplo.')
"

echo "✅ Build completed successfully!"
