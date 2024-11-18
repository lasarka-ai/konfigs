import zipfile
import os
from io import BytesIO

class VirtualFileSystem:
    def __init__(self, archive_path):
        if os.path.isdir(archive_path):  # Проверяем, папка это или файл
            self.root_path = archive_path
            self.zip_file = None
        elif os.path.isfile(archive_path):  # Если это файл, открываем как ZIP
            self.zip_file = zipfile.ZipFile(archive_path)
            self.root_path = None
        else:
            raise ValueError(f"{archive_path} не является ни папкой, ни архивом.")


    
    def list_directory(self, path='.'):
        # Если путь относительный, объединяем с текущей директорией
        if path == '.':
            path = self.current_dir
        elif not path.startswith('/'):
            path = os.path.join(self.current_dir, path)

        # Нормализуем путь
        normalized_path = os.path.normpath(path).replace('\\', '/').lstrip('/')

        # Убедимся, что путь заканчивается на `/`
        if not normalized_path.endswith('/'):
            normalized_path += '/'

        # Логируем текущий путь
        print(f"Listing directory: {normalized_path}")

        # Проверяем, есть ли файлы/папки в указанном пути
        items = []
        if self.zip_file:
            for name in self.zip_file.namelist():
                if name.startswith(normalized_path) and name != normalized_path:
                    # Получаем относительный путь
                    relative_path = name[len(normalized_path):]
                    # Проверяем, является ли элемент файлом или папкой
                    if '/' not in relative_path or relative_path.endswith('/'):
                        items.append(relative_path.rstrip('/'))

        return sorted(items)


    
    def change_directory(self, path):
        # Определяем полный путь
        if path.startswith('/'):
            new_path = path
        else:
            new_path = os.path.join(self.current_dir, path)

        # Нормализуем путь
        new_path = os.path.normpath(new_path).replace('\\', '/')

        # Убираем начальный слэш для сравнения с архивом
        normalized_path = new_path.lstrip('/')

        # Проверяем, чтобы путь заканчивался на `/`
        if not normalized_path.endswith('/'):
            normalized_path += '/'

        # Логируем текущий путь и список архивных путей
        print(f"Attempting to change directory to: {new_path} (normalized: {normalized_path})")
        print("Current archive paths:")
        for archive_path in self.zip_file.namelist():
            print(f" - {archive_path}")

        # Проверяем существование директории
        path_exists = any(normalized_path == archive_path for archive_path in self.zip_file.namelist())
        print(f"Path {normalized_path} exists: {path_exists}")

        if not path_exists:
            raise Exception(f'No such directory: {path}')

        # Обновляем текущую директорию
        self.current_dir = normalized_path
        print(f"Changed directory to: {self.current_dir}")


    
    def get_current_directory(self):
        return self.current_dir