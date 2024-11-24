import argparse
import os
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
    
    print(f"\nRepository Analysis Settings:")
    print(f"Repository path: {args.repo_path}")
    print(f"Output file: {args.output}")
    print(f"Date limit: {args.date}")
    
    try:
        date_limit = datetime.strptime(args.date, '%Y-%m-%d')
        print(f"Parsed date limit: {date_limit}")
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return 1
    
    try:
        # Проверяем наличие .git директории
        git_dir = os.path.join(args.repo_path, '.git')
        if not os.path.exists(git_dir):
            print(f"Warning: .git directory not found at {git_dir}")
            print("Make sure you're using the correct repository path")
            return 1
        
        print("\nStarting repository analysis...")
        analyzer = GitAnalyzer(args.repo_path)
        commits_data = analyzer.analyze_commits(date_limit)
        
        if not commits_data:
            print("\nNo commits found before the specified date")
            return 1
            
        print(f"\nBuilding dependency graph for {len(commits_data)} commits...")
        graph_builder = GraphBuilder()
        dependency_graph = graph_builder.build_graph(commits_data)
        
        print(f"\nGenerating PlantUML visualization...")
        plantuml_gen = PlantUMLGenerator()
        plantuml_code = plantuml_gen.generate(dependency_graph)
        
        output_dir = os.path.dirname(os.path.abspath(args.output))
        os.makedirs(output_dir, exist_ok=True)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
            
        print(f"\nSuccess! Graph has been generated and saved to: {args.output}")
        return 0
        
    except Exception as e:
        print(f"\nError during execution: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())