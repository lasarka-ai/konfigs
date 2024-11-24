import unittest
from datetime import datetime
from unittest.mock import Mock, patch
from src.git_analyzer import GitAnalyzer

class TestGitAnalyzer(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        with patch('src.git_analyzer.Repo') as mock_repo_class:
            mock_repo_class.return_value = self.mock_repo
            self.analyzer = GitAnalyzer('/fake/path')

    def test_analyze_commits(self):
        # Подготовка тестовых данных
        mock_commit = Mock()
        mock_commit.hexsha = 'abc123'
        mock_commit.committed_date = datetime(2024, 1, 1).timestamp()
        mock_commit.parents = []
        
        self.mock_repo.iter_commits.return_value = [mock_commit]
        
        # Выполнение теста
        date_limit = datetime(2024, 2, 1)
        result = self.analyzer.analyze_commits(date_limit)
        
        # Проверки
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['hash'], 'abc123')