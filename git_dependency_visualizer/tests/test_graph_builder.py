import unittest
from src.graph_builder import GraphBuilder

class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = GraphBuilder()

    def test_build_graph(self):
        # Тестовые данные
        commits_data = [{
            'hash': 'abc123',
            'date': '2024-01-01',
            'files': {'src/main.py', 'tests/test_main.py'}
        }]
        
        # Выполнение теста
        graph = self.builder.build_graph(commits_data)
        
        # Проверки
        self.assertIn('abc123', graph['commit_nodes'])
        self.assertIn('src/main.py', graph['file_nodes'])
        self.assertIn('src', graph['file_nodes'])