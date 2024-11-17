import argparse
import sys
from shell_gui import ShellGUI
from utils.file_system import VirtualFileSystem
from utils.logger import Logger

def parse_arguments():
    parser = argparse.ArgumentParser(description='Shell Emulator')
    parser.add_argument('--hostname', required=True, help='Hostname for shell prompt')
    parser.add_argument('--fs-archive', required=True, help='Path to filesystem archive (zip)')
    parser.add_argument('--log-file', required=True, help='Path to log file (json)')
    parser.add_argument('--startup-script', help='Path to startup script')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Initialize virtual filesystem
    fs = VirtualFileSystem(args.fs_archive)
    
    # Initialize logger
    logger = Logger(args.log_file)
    
    # Create and start GUI
    app = ShellGUI(args.hostname, fs, logger)
    if args.startup_script:
        app.execute_startup_script(args.startup_script)
    app.run()

if __name__ == '__main__':
    main()