from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Force reset database in production'

    def handle(self, *args, **options):
        self.stdout.write('⚠️ RESETTING DATABASE...')
        
        with connection.cursor() as cursor:
            # Drop all tables that might exist
            cursor.execute("""
                DROP TABLE IF EXISTS jogos_partida CASCADE;
                DROP TABLE IF EXISTS jogos_dupla_jogadores CASCADE;
                DROP TABLE IF EXISTS jogos_dupla CASCADE;
                DROP TABLE IF EXISTS jogos_jogador CASCADE;
            """)
            
            self.stdout.write('🗑️ Dropped existing tables')
            
        # Now run migrations
        from django.core.management import call_command
        call_command('migrate', verbosity=2)
        
        self.stdout.write('✅ Database reset complete!')
