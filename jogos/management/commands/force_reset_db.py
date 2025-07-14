from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Force reset database in production'

    def handle(self, *args, **options):
        self.stdout.write('⚠️ RESETTING DATABASE...')
        
        with connection.cursor() as cursor:
            # First, drop all foreign key constraints
            cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                    END LOOP;
                END $$;
            """)
            
            self.stdout.write('🗑️ Dropped all existing tables')
            
            # Clear django_migrations table for our app
            cursor.execute("""
                DELETE FROM django_migrations WHERE app = 'jogos';
            """)
            
            self.stdout.write('🧹 Cleared migration history')
            
        self.stdout.write('✅ Database reset complete!')
