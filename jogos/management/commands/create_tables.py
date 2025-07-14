from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Create tables directly using SQL'

    def handle(self, *args, **options):
        self.stdout.write('🔨 Creating tables directly...')
        
        with connection.cursor() as cursor:
            # Create tables in correct order
            
            # 1. Jogador table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogos_jogador (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL
                );
            """)
            self.stdout.write('✅ Created jogos_jogador')
            
            # 2. Dupla table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogos_dupla (
                    id SERIAL PRIMARY KEY
                );
            """)
            self.stdout.write('✅ Created jogos_dupla')
            
            # 3. Dupla-Jogadores many-to-many table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogos_dupla_jogadores (
                    id SERIAL PRIMARY KEY,
                    dupla_id INTEGER REFERENCES jogos_dupla(id) ON DELETE CASCADE,
                    jogador_id INTEGER REFERENCES jogos_jogador(id) ON DELETE CASCADE,
                    UNIQUE(dupla_id, jogador_id)
                );
            """)
            self.stdout.write('✅ Created jogos_dupla_jogadores')
            
            # 4. Partida table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogos_partida (
                    id SERIAL PRIMARY KEY,
                    data DATE NOT NULL DEFAULT CURRENT_DATE,
                    pontos_dupla1 INTEGER NOT NULL CHECK (pontos_dupla1 >= 0),
                    pontos_dupla2 INTEGER NOT NULL CHECK (pontos_dupla2 >= 0),
                    dupla1_id INTEGER NOT NULL REFERENCES jogos_dupla(id) ON DELETE CASCADE,
                    dupla2_id INTEGER NOT NULL REFERENCES jogos_dupla(id) ON DELETE CASCADE
                );
            """)
            self.stdout.write('✅ Created jogos_partida')
            
            # Mark migrations as applied
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('jogos', '0001_initial', NOW())
                ON CONFLICT (app, name) DO NOTHING;
            """)
            
            self.stdout.write('✅ Tables created successfully!')
