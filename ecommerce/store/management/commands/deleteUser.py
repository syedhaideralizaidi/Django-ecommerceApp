from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run to delete a user'
    def add_arguments(self, parser):
        #parser.add_argument('name',type = str, help='Enter the name')
        parser.add_argument('user_id',nargs='+', type= int, help='User id')
    def handle(self, *args, **kwargs):
       users = kwargs['user_id']

       for user_id in users:
           try:
               user = User.objects.get(pk= user_id)
               user.delete()

               self.stdout.write('"%s (%s)" has been deleted!' %(user.username,user_id))
           except User.DoesNotExist:
               self.stdout.write('User is not in the database')