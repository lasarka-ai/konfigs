import unittest
import os
import sys
import shutil
import tempfile
from datetime import datetime
from git import Repo
import subprocess
import gc
import coverege
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

try:
    from src.git_analyzer import GitAnalyzer
    from src.graph_builder import GraphBuilder
    from src.plantuml_generator import PlantUMLGenerator
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")
    raise

class TestGitAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем временную директорию для всех тестов"""
        cls.base_test_dir = tempfile.mkdtemp()
        print(f"\nTest directory created at: {cls.base_test_dir}")

    def setUp(self):
        """Настройка для каждого теста"""
        self.test_dir = os.path.join(self.base_test_dir, f'test_repo_{id(self)}')
        self.repo_path = os.path.join(self.test_dir, 'test_repo')
        os.makedirs(self.repo_path, exist_ok=True)
        
        self.repo = Repo.init(self.repo_path)
        
        with self.repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        self._create_test_repository()
        
        self.output_dir = os.path.join(self.test_dir, 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_puml = os.path.join(self.output_dir, 'graph.puml')

    def tearDown(self):
        """Очистка после каждого теста"""
        try:
            if hasattr(self, 'repo'):
                self.repo.close()
            
            gc.collect()
            time.sleep(1)
            
            if os.path.exists(self.test_dir):
                shutil.rmtree(self.test_dir, onerror=self._handle_remove_readonly)
        except Exception as e:
            print(f"Warning: Error during tearDown: {e}")

    @classmethod
    def tearDownClass(cls):
        """Очистка после всех тестов"""
        try:
            # выпуск мусоровоза, т.к. ошибку сыпт мол я что то  почистил, хз может сработает. (P.S. Вроде сработало)
            gc.collect()
            time.sleep(1)
            
            if os.path.exists(cls.base_test_dir):
                shutil.rmtree(cls.base_test_dir, onerror=cls._handle_remove_readonly)
        except Exception as e:
            print(f"Warning: Error during tearDownClass: {e}")

    @staticmethod
    def _handle_remove_readonly(func, path, exc):
        """Обработчик для удаления read-only файлов"""
        import stat
        if func in (os.rmdir, os.remove, os.unlink) and exc[1].errno == 13:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise exc

    def _create_test_repository(self):
        """Создаем тестовую структуру репозитория"""
        try:
            #труктура директорий
            os.makedirs(os.path.join(self.repo_path, 'src'), exist_ok=True)
            os.makedirs(os.path.join(self.repo_path, 'tests'), exist_ok=True)
            
            # коммитим файлы
            test_files = {
                'src/main.py': 'print("Hello, World!")',
                'src/utils.py': 'def greet(): return "Hello"',
                'tests/test_main.py': 'def test_main(): pass',
                'README.md': '# Test Repository'
            }
            
            for file_path, content in test_files.items():
                full_path = os.path.join(self.repo_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                with open(full_path, 'w') as f:
                    f.write(content)
                
                self.repo.index.add([file_path])
                self.repo.index.commit(f"Add {file_path}")
        except Exception as e:
            print(f"Error in _create_test_repository: {e}")
            raise

    def test_git_analyzer_initialization(self):
        """Проверка инициализации анализатора"""
        analyzer = GitAnalyzer(self.repo_path)
        self.assertIsNotNone(analyzer)
        self.assertEqual(analyzer.repo_path, self.repo_path)

    def test_analyze_commits(self):
        """Проверка анализа коммитов"""
        analyzer = GitAnalyzer(self.repo_path)
        future_date = datetime(2025, 1, 1)
        commits_data = analyzer.analyze_commits(future_date)
        
        self.assertEqual(len(commits_data), 4)  # 4 файла = 4 коммита
        
        first_commit = commits_data[0]
        required_fields = ['hash', 'date', 'files', 'message']
        for field in required_fields:
            self.assertIn(field, first_commit)

    def test_graph_builder(self):
        """Проверка построения графа"""
        analyzer = GitAnalyzer(self.repo_path)
        commits_data = analyzer.analyze_commits(datetime(2025, 1, 1))
        
        builder = GraphBuilder()
        graph = builder.build_graph(commits_data)
        
        required_keys = ['nodes', 'edges', 'file_nodes', 'commit_nodes']
        for key in required_keys:
            self.assertIn(key, graph)
            self.assertIsInstance(graph[key], set)
            self.assertGreater(len(graph[key]), 0)

    def test_full_pipeline_with_files(self):
        """Проверка полного процесса с генерацией файлов"""
        try:
            analyzer = GitAnalyzer(self.repo_path)
            commits_data = analyzer.analyze_commits(datetime(2025, 1, 1))
            
            builder = GraphBuilder()
            graph = builder.build_graph(commits_data)
            
            generator = PlantUMLGenerator()
            puml_code = generator.generate(graph)
            
            os.makedirs(os.path.dirname(self.output_puml), exist_ok=True)
            with open(self.output_puml, 'w', encoding='utf-8') as f:
                f.write(puml_code)
            
            self.assertTrue(os.path.exists(self.output_puml), 
                        "PUML file was not generated")
            
            with open(self.output_puml, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('@startuml', content)
                self.assertIn('@enduml', content)
                
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")

    def test_invalid_repository_path(self):
        """Проверка обработки неверного пути к репозиторию"""
        invalid_path = os.path.join(self.test_dir, 'nonexistent_repo')
        with self.assertRaises(ValueError):
            GitAnalyzer(invalid_path)

if __name__ == '__main__':
    unittest.main()