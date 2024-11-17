import getpass
import datetime
from .base_command import BaseCommand

class WhoCommand(BaseCommand):
    def execute(self, args):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        return f'{getpass.getuser()}  console  {current_time}'

class WhoamiCommand(BaseCommand):
    def execute(self, args):
        return getpass.getuser()