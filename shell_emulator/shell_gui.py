from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from commands.filesystem_commands import LSCommand, CDCommand
from commands.user_commands import WhoCommand, WhoamiCommand
from commands.text_commands import UniqCommand

class ShellGUI(QMainWindow):
    def __init__(self, hostname, filesystem, logger):
        super().__init__()
        self.hostname = hostname
        self.fs = filesystem
        self.logger = logger
        self.init_ui()
        
        # Initialize commands
        self.commands = {
            'ls': LSCommand(self.fs, self.logger),
            'cd': CDCommand(self.fs, self.logger),
            'who': WhoCommand(self.logger),
            'whoami': WhoamiCommand(self.logger),
            'uniq': UniqCommand(self.fs, self.logger),
            'exit': self.close
        }
    
    def init_ui(self):
        self.setWindowTitle(f'Shell Emulator - {self.hostname}')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create output text area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)
        
        # Create input line
        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.process_command)
        layout.addWidget(self.input_line)
        
        central_widget.setLayout(layout)
        
        self.show_prompt()
    
    def show_prompt(self):
        self.output_area.append(f'{self.hostname}:~$ ')
    
    def process_command(self):
        command = self.input_line.text().strip()
        self.input_line.clear()
        
        if command:
            self.output_area.append(command)
            self.logger.log_command(command)
            
            parts = command.split()
            cmd_name = parts[0]
            args = parts[1:]
            
            if cmd_name in self.commands:
                try:
                    output = self.commands[cmd_name].execute(args)
                    if output:
                        self.output_area.append(output)
                except Exception as e:
                    self.output_area.append(f'Error: {str(e)}')
            else:
                self.output_area.append(f'Command not found: {cmd_name}')
        
        self.show_prompt()
    
    def execute_startup_script(self, script_path):
        try:
            with open(script_path, 'r') as f:
                commands = f.readlines()
            
            for command in commands:
                command = command.strip()
                if command and not command.startswith('#'):
                    self.input_line.setText(command)
                    self.process_command()
        except Exception as e:
            self.output_area.append(f'Error executing startup script: {str(e)}')
    
    def run(self):
        self.show()