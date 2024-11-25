import os
from git import Repo
from datetime import datetime
from typing import Dict, List, Set

class GitAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        if not os.path.exists(repo_path):
            raise ValueError(f"Repository path does not exist: {repo_path}")
        try:
            print(f"Initializing repository at: {repo_path}")
            self.repo = Repo(repo_path)
            print(f"Git directory: {self.repo.git_dir}")
            print(f"Working directory: {self.repo.working_dir}")
            
            if not self.repo.git_dir:
                raise ValueError("Not a valid Git repository")


            print(f"Active branch: {self.repo.active_branch.name}")
            print(f"Is bare repository: {self.repo.bare}")
            

            remotes = list(self.repo.remotes)
            print(f"Remote repositories: {[r.name for r in remotes]}")
            
        except Exception as e:
            raise ValueError(f"Error initializing Git repository: {str(e)}")
    
    def analyze_commits(self, date_limit: datetime) -> List[Dict[str, any]]:
        commits_data = []
        print(f"Analyzing commits before {date_limit}")
        
        try:
            all_commits = list(self.repo.iter_commits())
            print(f"Total commits in repository: {len(all_commits)}")
            
            for commit in all_commits:
                commit_date = datetime.fromtimestamp(commit.committed_date)
                print(f"Analyzing commit: {commit.hexsha[:7]} from {commit_date}")
                
                if commit_date > date_limit:
                    print(f"Skipping commit {commit.hexsha[:7]} - after date limit")
                    continue
                    
                changed_files = self._get_changed_files(commit)
                if changed_files:
                    commits_data.append({
                        'hash': commit.hexsha,
                        'date': commit_date,
                        'files': changed_files,
                        'message': commit.message.strip()
                    })
                    print(f"Added commit {commit.hexsha[:7]} with {len(changed_files)} changed files")
        
        except Exception as e:
            print(f"Error during commit analysis: {str(e)}")
            raise
        
        print(f"Total commits analyzed: {len(commits_data)}")
        return commits_data
    
    def _get_changed_files(self, commit) -> Set[str]:
        changed_files = set()
        
        try:
            if commit.parents:
                for parent in commit.parents:
                    diff = parent.diff(commit)
                    for diff_item in diff:
                        if diff_item.a_path:
                            changed_files.add(diff_item.a_path)
                        if diff_item.b_path and diff_item.b_path != diff_item.a_path:
                            changed_files.add(diff_item.b_path)
            else:
                for blob in commit.tree.traverse():
                    if blob.type == 'blob':
                        changed_files.add(blob.path)
            
            if changed_files:
                print(f"Files changed in commit {commit.hexsha[:7]}:")
                for file in changed_files:
                    print(f"  - {file}")
            
            return changed_files
            
        except Exception as e:
            print(f"Error analyzing commit {commit.hexsha}: {str(e)}")
            return set()