from typing import Dict, List, Set
from collections import defaultdict

class GraphBuilder:
    def build_graph(self, commits_data: List[Dict]) -> Dict[str, Set]:
        graph = {
            'nodes': set(),  # Все узлы (коммиты и файлы)
            'edges': set(),  # Связи между узлами
            'file_nodes': set(),  # Только файловые узлы
            'commit_nodes': set()  # Только узлы коммитов
        }
        
        for commit in commits_data:
            commit_hash = commit['hash']
            graph['commit_nodes'].add(commit_hash)
            graph['nodes'].add(commit_hash)
            
            # Добавляем связи между коммитом и файлами
            for file_path in commit['files']:
                graph['file_nodes'].add(file_path)
                graph['nodes'].add(file_path)
                graph['edges'].add((commit_hash, file_path))
                
                # Добавляем связи с родительскими директориями
                path_parts = file_path.split('/')
                current_path = ""
                for part in path_parts[:-1]:
                    if current_path:
                        current_path += '/'
                    current_path += part
                    graph['file_nodes'].add(current_path)
                    graph['nodes'].add(current_path)
                    if not current_path:
                        continue
                    graph['edges'].add((current_path, file_path))
        
        return graph
