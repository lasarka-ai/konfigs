import zipfile
import os

def create_test_filesystem():
    # Убедимся, что мы находимся в правильной директории
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, 'test_filesystem.zip')
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # Создаем директории
        directories = [
            'home/',
            'home/user/',
            'home/user/documents/',
            'home/user/downloads/',
            'usr/',
            'usr/local/',
            'etc/'
        ]
        
        for directory in directories:
            zf.writestr(directory, '')
        
        # Создаем тестовый файл
        test_content = 'Hello\nHello\nWorld\nWorld\nTest\n'
        zf.writestr('home/user/documents/test.txt', test_content)
        
        print(f"Created test filesystem at {zip_path}")

if __name__ == '__main__':
    create_test_filesystem()