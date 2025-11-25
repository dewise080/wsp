import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'This will create tables in database and import data to your system and create a superuser.'

    def handle(self, *args, **options):

        # MySQL database configuration
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']

        # Import data
        self.stdout.write('Importing data from db.sql to MySQL...')
        try:
            subprocess.run(['mysql', '-u', db_user, '-p{}'.format(db_password), '-h', 'localhost', db_name], input=open('db.sql', 'rb').read().decode('utf-8'), check=True, text=True, cwd=settings.BASE_DIR)
            self.stdout.write(self.style.SUCCESS(f'Data imported to {db_name} successfully.'))
            self.stdout.write(self.style.SUCCESS('Installation successfully completed.'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error importing data from db.sql to MySQL: {e}'))