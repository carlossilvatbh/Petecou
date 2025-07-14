from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Debug database tables and migrations'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Debugging database...')
        
        with connection.cursor() as cursor:
            # List all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cursor.fetchall()
            
            self.stdout.write(f'📋 Tables found: {len(tables)}')
            for table in tables:
                self.stdout.write(f'  - {table[0]}')
            
            # Check if jogos_jogador exists specifically
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'jogos_jogador'
                )
            """)
            jogador_exists = cursor.fetchone()[0]
            
            self.stdout.write(
                f'🎯 jogos_jogador table exists: {jogador_exists}'
            )
            
            # Check migration status
            cursor.execute("""
                SELECT app, name, applied 
                FROM django_migrations 
                WHERE app = 'jogos'
            """)
            migrations = cursor.fetchall()
            
            self.stdout.write('📦 Jogos migrations:')
            for app, name, applied in migrations:
                status = '✅' if applied else '❌'
                self.stdout.write(f'  {status} {app}.{name}')
