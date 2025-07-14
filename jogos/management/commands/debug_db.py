from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Debug database tables and migrations'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Debugging database...')
        
        try:
            with connection.cursor() as cursor:
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
                
                if jogador_exists:
                    cursor.execute("SELECT COUNT(*) FROM jogos_jogador")
                    count = cursor.fetchone()[0]
                    self.stdout.write(f'� Jogadores count: {count}')
                
        except Exception as e:
            self.stdout.write(f'❌ Debug error: {e}')
