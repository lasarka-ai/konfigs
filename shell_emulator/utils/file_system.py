import zipfile
import os
from io import BytesIO

class VirtualFileSystem:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.current_dir = '/'
        self.zip_file = zipfile.ZipFile(archive_path)
    
    def list_directory(self, path='.'):
        if path == '.':
            path = self.current_dir
        elif not path.startswith('/'):
            path = os.path.join(self.current_dir, path)
        
        path = os.path.normpath(path).replace('\\', '/')
        if not path.endswith('/'):
            path += '/'
        
        items = []
        for name in self.zip_file.namelist():
            if name.startswith(path) and name != path:
                relative_path = name[len(path):]
                if '/' not in relative_path or relative_path.endswith('/'):
                    items.append(relative_path.rstrip('/'))
        
        return sorted(items)
    
    def change_directory(self, path):
        if path.startswith('/'):
            new_path = path
        else:
            new_path = os.path.join(self.current_dir, path)
        
        new_path = os.path.normpath(new_path).replace('\\', '/')
        
        if not new_path.endswith('/'):
            new_path += '/'
        
        if new_path not in self.zip_file.namelist() and new_path != '/':
            raise Exception(f'No such directory: {path}')
        
        self.current_dir = new_path
    
    def get_current_directory(self):
        return self.current_dir