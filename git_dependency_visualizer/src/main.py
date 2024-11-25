import argparse
import os
import subprocess
from datetime import datetime
from git_analyzer import GitAnalyzer
from graph_builder import GraphBuilder
from plantuml_generator import PlantUMLGenerator

def parse_args():
    parser = argparse.ArgumentParser(description='Git dependency visualizer')
    parser.add_argument('--repo-path', required=True, help='Path to Git repository')
    parser.add_argument('--output', required=False, help='Path to output file (optional)')
    parser.add_argument('--date', required=True, help='Date limit (YYYY-MM-DD)')
    parser.add_argument('--viz-path', required=False, help='Path to visualization program (optional)')
    return parser.parse_args()

def main():
    args = parse_args()
    
    print(f"\nRepository Analysis Settings:")
    print(f"Repository path: {args.repo_path}")
    if args.output:
        print(f"Output file: {args.output}")
    print(f"Date limit: {args.date}")
    
    try:
        date_limit = datetime.strptime(args.date, '%Y-%m-%d')
        print(f"Parsed date limit: {date_limit}")
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return 1
    
    try:

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
        
        print("\nGraph Structure:")
        print(graph_builder.print_graph(dependency_graph))
        
        print(f"\nGenerating PlantUML visualization...")
        plantuml_gen = PlantUMLGenerator()
        plantuml_code = plantuml_gen.generate(dependency_graph)
        
        print("\nPlantUML Code:")
        print(plantuml_code)
        
        if args.output:
            output_dir = os.path.dirname(os.path.abspath(args.output))
            os.makedirs(output_dir, exist_ok=True)
            
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(plantuml_code)
            print(f"\nCode has been saved to: {args.output}")
        
        if args.viz_path and args.output:
            print(f"\nRunning visualizer...")
            try:
                if args.viz_path.endswith('.jar'):
                    process = subprocess.Popen(
                        ['java', '-jar', args.viz_path, args.output],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                else:
                    process = subprocess.Popen(
                        [args.viz_path, args.output],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    print(f"Visualization error: {stderr.decode()}")
                else:
                    print("Visualization completed successfully")
                    png_path = args.output.rsplit('.', 1)[0] + '.png'
                    if os.path.exists(png_path):
                        print(f"Generated image: {png_path}")
            except Exception as e:
                print(f"Error running visualizer: {str(e)}")

                



        return 0

    except Exception as e:
        print(f"\nError during execution: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())