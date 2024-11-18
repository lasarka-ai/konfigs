import zipfile
import os

def create_test_filesystem():
    with zipfile.ZipFile('test_filesystem.zip', 'w') as zf:
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
        
        print("Created test filesystem successfully")

if __name__ == '__main__':
    create_test_filesystem()