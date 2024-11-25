from typing import Dict, List, Set
from collections import defaultdict

class GraphBuilder:
    def build_graph(self, commits_data: List[Dict]) -> Dict[str, Set]:
        graph = {
            'nodes': set(), 
            'edges': set(), 
            'file_nodes': set(),  
            'commit_nodes': set() 
        }
        
        sorted_commits = sorted(commits_data, key=lambda x: x['date'])
        file_last_commit = {}
        
        for commit in sorted_commits:
            commit_hash = commit['hash']
            graph['commit_nodes'].add(commit_hash)
            graph['nodes'].add(commit_hash)
            
            for file_path in commit['files']:
                graph['file_nodes'].add(file_path)
                graph['nodes'].add(file_path)
                graph['edges'].add((commit_hash, file_path))
                
                if file_path in file_last_commit:
                    graph['edges'].add((file_last_commit[file_path], commit_hash))
                
                file_last_commit[file_path] = commit_hash
                
                path_parts = file_path.split('/')
                current_path = ""
                for part in path_parts[:-1]:
                    if current_path:
                        current_path += '/'
                    current_path += part
                    graph['file_nodes'].add(current_path)
                    graph['nodes'].add(current_path)
                    if current_path:
                        graph['edges'].add((current_path, file_path))
        
        return graph

    def print_graph(self, graph: Dict[str, Set]) -> str:
        """Выводит граф в виде текстового представления для отладки"""
        result = []
        result.append("Graph structure:")
        result.append("\nNodes:")
        for node in sorted(graph['nodes']):
            node_type = "Commit" if node in graph['commit_nodes'] else "File"
            result.append(f"  {node_type}: {node}")
        
        result.append("\nEdges:")
        for edge in sorted(graph['edges']):
            result.append(f"  {edge[0]} -> {edge[1]}")
            
        return "\n".join(result)