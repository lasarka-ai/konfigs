import argparse
from datetime import datetime
from git_analyzer import GitAnalyzer
from graph_builder import GraphBuilder
from plantuml_generator import PlantUMLGenerator

def parse_args():
    parser = argparse.ArgumentParser(description='Git dependency visualizer')
    parser.add_argument('--repo-path', required=True, help='Path to Git repository')
    parser.add_argument('--output', required=True, help='Path to output file')
    parser.add_argument('--date', required=True, help='Date limit (YYYY-MM-DD)')
    parser.add_argument('--viz-path', required=True, help='Path to visualization program')
    return parser.parse_args()

def main():
    args = parse_args()
    
    try:
        date_limit = datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return 1
    
    try:
        # Анализ репозитория
        analyzer = GitAnalyzer(args.repo_path)
        commits_data = analyzer.analyze_commits(date_limit)
        
        # Построение графа
        graph_builder = GraphBuilder()
        dependency_graph = graph_builder.build_graph(commits_data)
        
        # Генерация PlantUML
        plantuml_gen = PlantUMLGenerator()
        plantuml_code = plantuml_gen.generate(dependency_graph)
        
        # Сохранение результата
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
            
        print(f"Graph has been generated and saved to {args.output}")
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())