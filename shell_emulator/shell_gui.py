from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from commands.filesystem_commands import LSCommand, CDCommand
from commands.user_commands import WhoCommand, WhoamiCommand
from commands.text_commands import UniqCommand
import os

class ShellGUI(QMainWindow):
    def __init__(self, hostname, filesystem, logger):
        super().__init__()
        self.hostname = hostname
        self.fs = filesystem
        self.logger = logger
        
        if not hasattr(self.fs, 'current_dir'):
            self.fs.current_dir = os.path.expanduser('~')
        
        self.init_ui()
        self.commands = {
            'ls': LSCommand(self.fs, self.logger),
            'cd': CDCommand(self.fs, self.logger),
            'who': WhoCommand(self.logger),
            'whoami': WhoamiCommand(self.logger),
            'uniq': UniqCommand(self.fs, self.logger),
            'exit': self.close
        }
        
        self.command_history = []
        self.history_index = -1
    
    def init_ui(self):
        self.setWindowTitle(f'Shell Emulator - {self.hostname}')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            background-color: #f4f4f4;
            color: #000;
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            padding: 10px;
        """)
        
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("""
            background-color: #ffffff;
            color: #000;
            font-family: 'Courier New', monospace;
            font-size: 12pt;
            padding: 5px;
            border: 1px solid #ccc;
        """)
        self.input_line.returnPressed.connect(self.process_command)
        
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)
        
        central_widget.setLayout(layout)
        
        self.input_line.installEventFilter(self)
        
        self.show_prompt()
    
    def show_prompt(self):
        """
        Updates the command prompt to display the hostname and current directory.
        """
        current_dir = self.fs.current_dir
        prompt = f'{self.hostname}:{current_dir}$ '
        self.output_area.append(prompt)
        
        self.output_area.verticalScrollBar().setValue(
            self.output_area.verticalScrollBar().maximum()
        )
    
    def process_command(self):
        """
        Processes user input and executes the appropriate command.
        """
        command = self.input_line.text().strip()
        self.input_line.clear()
        
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
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
    
    def eventFilter(self, source, event):
        """
        Handle special key events in the input line
        """
        if source == self.input_line and event.type() == QEvent.KeyPress:
            key = event.key()
            
            if key == Qt.Key_Up:
                if 0 <= self.history_index - 1 < len(self.command_history):
                    self.history_index -= 1
                    self.input_line.setText(self.command_history[self.history_index])
            
            elif key == Qt.Key_Down:
                if self.history_index < len(self.command_history) - 1:
                    self.history_index += 1
                    self.input_line.setText(self.command_history[self.history_index])
                else:
                    self.input_line.clear()
        
        return super().eventFilter(source, event)
    
    def execute_startup_script(self, script_path):
        """
        Executes a startup script with a sequence of commands.
        """
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
        """
        Launches the GUI.
        """
        self.show()