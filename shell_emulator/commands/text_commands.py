from .base_command import BaseCommand
import os

class UniqCommand(BaseCommand):
    def __init__(self, filesystem, logger):
        super().__init__(logger)
        self.fs = filesystem
    
    def execute(self, args):
        if not args:
            return 'uniq: missing operand'
        
        # Преобразуем путь в абсолютный
        file_path = args[0]
        if not file_path.startswith('/'):
            file_path = os.path.join(self.fs.get_current_directory(), file_path)
        
        try:
            # Открываем файл из zip архива
            with self.fs.zip_file.open(file_path, 'r') as f:
                lines = f.read().decode().splitlines()
            
            unique_lines = []
            prev_line = None
            
            for line in lines:
                if line != prev_line:
                    unique_lines.append(line)
                    prev_line = line
            
            return '\n'.join(unique_lines)
        except KeyError:
            return f'uniq: No such file or directory: {args[0]}'
        except Exception as e:
            return f'uniq: {str(e)}'
