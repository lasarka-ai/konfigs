import unittest
from src.plantuml_generator import PlantUMLGenerator

class TestPlantUMLGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PlantUMLGenerator()

    def test_generate(self):
        # Тестовые данные
        graph = {
            'nodes': {'commit1', 'file1'},
            'edges': {('commit1', 'file1')},
            'file_nodes': {'file1'},
            'commit_nodes': {'commit1'}
        }
        
        # Выполнение теста
        result = self.generator.generate(graph)
        
        # Проверки
        self.assertIn('@startuml', result)
        self.assertIn('@enduml', result)
        self.assertIn('component "commit1"', result)
        self.assertIn('file "file1"', result)