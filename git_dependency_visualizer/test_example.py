import os
from datetime import datetime, timedelta

# Конфигурация для тестового запуска
CONFIG = {
    'repo_path': r'C:\Users\User\Documents\GitHub\konfigs',
    'output_file': r'C:\Users\User\Documents\GitHub\konfigs\git_dependency_visualizer\result.puml',
    'viz_path': r'C:\Users\User\Documents\GitHub\konfigs\git_dependency_visualizer',  # В данном случае не используется
    'date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # Последние 7 дней
}

def main():
    # Создаем команду для запуска
    command = f'''python src/main.py \
        --repo-path "{CONFIG['repo_path']}" \
        --output "{CONFIG['output_file']}" \
        --date {CONFIG['date']} \
        --viz-path "{CONFIG['viz_path']}"'''
    
    # Выполняем команду
    print("Executing command:")
    print(command)
    os.system(command)

if __name__ == '__main__':
    main()