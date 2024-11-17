from .base_command import BaseCommand

class LSCommand(BaseCommand):
    def __init__(self, filesystem, logger):
        super().__init__(logger)
        self.fs = filesystem
    
    def execute(self, args):
        path = args[0] if args else '.'
        try:
            items = self.fs.list_directory(path)
            return '\n'.join(items)
        except Exception as e:
            return f'ls: {str(e)}'

class CDCommand(BaseCommand):
    def __init__(self, filesystem, logger):
        super().__init__(logger)
        self.fs = filesystem
    
    def execute(self, args):
        if not args:
            return 'cd: missing operand'
        try:
            self.fs.change_directory(args[0])
            return ''
        except Exception as e:
            return f'cd: {str(e)}'