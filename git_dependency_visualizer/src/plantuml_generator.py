from typing import Dict, Set

class PlantUMLGenerator:
    def generate(self, graph: Dict) -> str:
        if not graph['commit_nodes']:
            raise ValueError("No commits found in the graph")
            
        plantuml_code = ["@startuml"]
        
        # Определяем стили
        plantuml_code.extend([
            "skinparam roundcorner 20",
            "skinparam componentStyle uml2",
            "skinparam backgroundColor transparent",
            "",
            "' Стили для коммитов",
            "skinparam component {",
            "  BackgroundColor LightBlue",
            "  BorderColor Black",
            "}",
            "",
            "' Стили для файлов",
            "skinparam file {",
            "  BackgroundColor LightGreen",
            "  BorderColor Black",
            "}",
            "",
            "' Стили для папок",
            "skinparam folder {",
            "  BackgroundColor LightYellow",
            "  BorderColor Black",
            "}",
            ""
        ])
        
        # Добавляем узлы коммитов с метками даты
        for commit_hash in sorted(graph['commit_nodes']):
            short_hash = commit_hash[:7]
            plantuml_code.append(f'component "{short_hash}" as commit_{short_hash}')
        
        # Добавляем узлы файлов и папок
        for file_path in sorted(graph['file_nodes']):
            safe_id = self._safe_id(file_path)
            if '/' in file_path or '\\' in file_path:
                plantuml_code.append(f'folder "{file_path}" as {safe_id}')
            else:
                plantuml_code.append(f'file "{file_path}" as {safe_id}')
        
        # Добавляем связи
        for source, target in sorted(graph['edges']):
            source_id = f"commit_{source[:7]}" if source in graph['commit_nodes'] else self._safe_id(source)
            target_id = f"commit_{target[:7]}" if target in graph['commit_nodes'] else self._safe_id(target)
            plantuml_code.append(f'{source_id} --> {target_id}')
        
        plantuml_code.append("@enduml")
        return "\n".join(plantuml_code)
    
    def _safe_id(self, name: str) -> str:
        """Создает безопасный идентификатор для PlantUML"""
        return "id_" + name.replace('/', '_').replace('\\', '_').replace('.', '_').replace('-', '_').replace(' ', '_')