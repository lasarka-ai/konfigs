from .base_command import BaseCommand

class UniqCommand(BaseCommand):
    def execute(self, args):
        if not args:
            return 'uniq: missing operand'
        try:
            with open(args[0], 'r') as f:
                lines = f.readlines()
            
            unique_lines = []
            prev_line = None
            
            for line in lines:
                line = line.strip()
                if line != prev_line:
                    unique_lines.append(line)
                    prev_line = line
            
            return '\n'.join(unique_lines)
        except Exception as e:
            return f'uniq: {str(e)}'