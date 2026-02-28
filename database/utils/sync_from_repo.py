#!/usr/bin/env python3
"""
Sync From Repository - Scan and populate databases from repository files

This script is LOCATION-AGNOSTIC and COMPREHENSIVE:
- Scans the entire repository recursively
- Finds projects, stakeholders, and documents anywhere they exist
- Doesn't rely on specific directory structures
- Authoritative source of truth for all enterprise data

Usage:
    python sync_from_repo.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from db_manager import get_db_manager


class RepositorySync:
    """Sync data from repository to databases - LOCATION AGNOSTIC"""
    
    def __init__(self, repo_root: Path):
        """Initialize repository sync
        
        Args:
            repo_root: Root path of repository
        """
        self.repo_root = repo_root
        self.db_manager = get_db_manager()
        self.stats = {
            'projects_found': 0,
            'projects_added': 0,
            'projects_updated': 0,
            'docs_found': 0,
            'docs_added': 0,
            'stakeholder_docs_found': 0,
            'stakeholder_docs_added': 0
        }
        
        # Directories to exclude from scanning
        self.exclude_dirs = {
            '.git', 'node_modules', '__pycache__', '.cache', 'dist', 'build',
            '.venv', 'venv', '.env', 'target', 'coverage', '.admin', 'data',
            '.bin', '.idea', '.vscode'
        }
    
    def sync_all(self):
        """Sync all data from repository - COMPREHENSIVE SCAN"""
        print("=" * 70)
        print("REPOSITORY SYNC - Enterprise Backend Database")
        print("LOCATION-AGNOSTIC & COMPREHENSIVE")
        print("=" * 70)
        print()
        
        # Sync projects - scan entire repo
        print("📁 Syncing Projects (scanning entire repository)...")
        self.sync_projects()
        print()
        
        # Sync stakeholder documents - scan entire repo
        print("📄 Syncing Stakeholder Documents (comprehensive scan)...")
        self.sync_stakeholder_docs()
        print()
        
        # Sync public documentation - scan entire repo
        print("📚 Syncing Public Documentation (comprehensive scan)...")
        self.sync_public_docs()
        print()
        
        # Print statistics
        self.print_stats()
    
    def _should_skip_dir(self, dir_path: Path) -> bool:
        """Check if directory should be skipped
        
        Args:
            dir_path: Path to check
            
        Returns:
            True if should skip, False otherwise
        """
        # Check if any part of the path is in exclude list
        for part in dir_path.parts:
            if part in self.exclude_dirs or part.startswith('.'):
                return True
        return False
    
    def sync_projects(self):
        """Sync projects - AUTHORITATIVE scan of entire repository
        
        Finds projects by looking for:
        - Directories under enterprise/projects/ (primary project location)
        - Directories with package.json, Cargo.toml, go.mod, etc. elsewhere
        - Any directory that looks like a project (while skipping infrastructure dirs)
        """
        print("  🔍 Scanning repository for projects...")
        
        # Get existing projects
        existing_projects = self.db_manager.query('projects_db', 'projects')
        existing_map = {p['project_name']: p for p in existing_projects}
        
        # Directories that are NOT projects even though they have README.md
        non_project_dirs = {
            str(self.repo_root),  # Repo root
            str(self.repo_root / 'enterprise'),
            str(self.repo_root / 'database'),
            str(self.repo_root / 'docs'),
            str(self.repo_root / 'admin'),
            str(self.repo_root / 'copilot'),
            str(self.repo_root / 'notion'),
            str(self.repo_root / 'obsidian'),
            str(self.repo_root / 'scripts'),
            str(self.repo_root / 'tools'),
            str(self.repo_root / 'reports'),
        }
        
        # ── Primary: scan enterprise/projects/ for project directories ──
        projects_dir = self.repo_root / 'enterprise' / 'projects'
        found_projects = set()
        
        if projects_dir.exists():
            for child in sorted(projects_dir.iterdir()):
                if child.is_dir() and not child.name.startswith('.'):
                    found_projects.add(str(child))
                    self.stats['projects_found'] += 1
                    project_info = self._extract_project_info(child)
                    if project_info:
                        project_name = project_info['project_name']
                        if project_name in existing_map:
                            self.db_manager.update_record(
                                'projects_db', 'projects',
                                existing_map[project_name]['id'],
                                project_info
                            )
                            self.stats['projects_updated'] += 1
                            print(f"  ✓ Updated: {project_name}")
                        else:
                            self.db_manager.add_record('projects_db', 'projects', project_info)
                            self.stats['projects_added'] += 1
                            print(f"  ✓ Added: {project_name}")
        
        # ── Secondary: scan rest of repo for project-like directories ──
        for root, dirs, files in os.walk(self.repo_root):
            root_path = Path(root)
            
            if self._should_skip_dir(root_path):
                dirs[:] = []
                continue
            
            dirs[:] = [d for d in dirs if not (d in self.exclude_dirs or d.startswith('.'))]
            
            # Skip non-project infrastructure directories
            if str(root_path) in non_project_dirs:
                continue
            
            # Skip anything already found under enterprise/projects/
            if any(root_path == Path(p) or root_path.is_relative_to(Path(p)) for p in found_projects):
                continue
            
            # Skip database directory
            if 'database' in str(root_path.relative_to(self.repo_root)).split(os.sep):
                continue
            
            # Check for strong project indicators (not just README.md)
            strong_indicators = ['package.json', 'Cargo.toml', 'go.mod',
                                'pom.xml', 'build.gradle', 'setup.py', 'pyproject.toml',
                                'Makefile', 'CMakeLists.txt']
            
            is_project = any(ind in files for ind in strong_indicators)
            
            if not is_project:
                continue
                
            found_projects.add(str(root_path))
            self.stats['projects_found'] += 1
            project_info = self._extract_project_info(root_path)
            
            if project_info:
                project_name = project_info['project_name']
                if project_name in existing_map:
                    self.db_manager.update_record(
                        'projects_db', 'projects',
                        existing_map[project_name]['id'],
                        project_info
                    )
                    self.stats['projects_updated'] += 1
                    print(f"  ✓ Updated: {project_name}")
                else:
                    self.db_manager.add_record('projects_db', 'projects', project_info)
                    self.stats['projects_added'] += 1
                    print(f"  ✓ Added: {project_name}")
        
        print(f"  📊 Found {self.stats['projects_found']} projects in repository")
    
    def _extract_project_info(self, project_dir: Path) -> Dict[str, Any]:
        """Extract project information from directory
        
        Args:
            project_dir: Path to project directory
            
        Returns:
            Project information dictionary
        """
        project_name = project_dir.name
        
        # Initialize project data
        project_data = {
            'project_name': project_name,
            'status': 'Active',
            'category': self._guess_category(project_name),
            'priority': 'P2 Medium',
            'lifecycle_stage': 'Development',
            'health_score': 80,
            'progress': 0,
            'open_source': False,
            'tech_stack': [],
            'tags': []
        }
        
        # Look for README
        readme_path = project_dir / "README.md"
        if readme_path.exists():
            project_data['readme_path'] = str(readme_path.relative_to(self.repo_root))
            readme_content = readme_path.read_text(encoding='utf-8', errors='ignore')
            
            # Extract description (first paragraph after heading)
            lines = readme_content.split('\n')
            description_lines = []
            found_heading = False
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    found_heading = True
                    continue
                if found_heading and line and not line.startswith('#'):
                    description_lines.append(line)
                    if len(description_lines) >= 3:  # Get first few lines
                        break
            
            if description_lines:
                project_data['description'] = ' '.join(description_lines)[:500]
            
            # Check for GitHub repo link
            github_match = re.search(r'github\.com/[\w-]+/[\w-]+', readme_content)
            if github_match:
                project_data['github_repository'] = f"https://{github_match.group(0)}"
            
            # Check for license
            if 'MIT' in readme_content:
                project_data['license'] = 'MIT'
                project_data['open_source'] = True
            elif 'Apache' in readme_content:
                project_data['license'] = 'Apache-2.0'
                project_data['open_source'] = True
            elif 'GPL' in readme_content:
                project_data['license'] = 'GPL-3.0'
                project_data['open_source'] = True
        
        return project_data
    
    def _guess_category(self, project_name: str) -> str:
        """Guess project category from name"""
        name_lower = project_name.lower()
        
        if any(x in name_lower for x in ['ai', 'ml', 'ava', 'research']):
            return 'AI/ML & Research'
        elif any(x in name_lower for x in ['blockchain', 'chain', 'crypto']):
            return 'Blockchain'
        elif any(x in name_lower for x in ['erp', 'enterprise', 'artifact-erp']):
            return 'Enterprise'
        elif any(x in name_lower for x in ['sdk', 'tool', 'dev']):
            return 'Developer Tools'
        elif any(x in name_lower for x in ['collab', 'comm', 'social']):
            return 'Collaboration'
        else:
            return 'Flagship Products'
    
    def sync_stakeholder_docs(self):
        """Sync stakeholder documents - AUTHORITATIVE scan
        
        Finds stakeholder documents by:
        - Scanning for markdown files with 'stakeholder' in path/name
        - Looking for business documents
        - Checking for internal classification markers
        """
        print("  🔍 Scanning repository for stakeholder documents...")
        
        # Scan entire repository for stakeholder-related markdown files
        for root, dirs, files in os.walk(self.repo_root):
            root_path = Path(root)
            
            # Skip excluded directories
            if self._should_skip_dir(root_path):
                dirs[:] = []
                continue
            
            dirs[:] = [d for d in dirs if not (d in self.exclude_dirs or d.startswith('.'))]
            
            for file in files:
                if not file.endswith('.md') or file.startswith('.'):
                    continue
                
                file_path = root_path / file
                
                # Determine if this is a stakeholder document
                is_stakeholder_doc = False
                path_str = str(file_path.relative_to(self.repo_root)).lower()
                
                # Check if path contains stakeholder-related keywords
                stakeholder_keywords = ['stakeholder', 'business', 'executive', 'partner',
                                       'investor', 'board', 'strategic', 'client', 'customer']
                
                if any(keyword in path_str for keyword in stakeholder_keywords):
                    is_stakeholder_doc = True
                
                if not is_stakeholder_doc:
                    continue
                
                self.stats['stakeholder_docs_found'] += 1
                
                # Read content
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    doc_data = {
                        'title': file_path.stem.replace('-', ' ').replace('_', ' ').title(),
                        'type': self._guess_doc_type(file_path.name),
                        'category': 'Stakeholder',
                        'content': content[:5000],  # Limit content size
                        'file_path': str(file_path.relative_to(self.repo_root)),
                        'status': 'Published',
                        'published_date': datetime.utcnow().date().isoformat(),
                        'tags': ['stakeholder', 'internal']
                    }
                    
                    # Check if already exists
                    existing = self.db_manager.query('internal_db', 'internal_documents', 
                                                    {'file_path': doc_data['file_path']})
                    
                    if not existing:
                        self.db_manager.add_record('internal_db', 'internal_documents', doc_data)
                        self.stats['stakeholder_docs_added'] += 1
                        print(f"  ✓ Added: {doc_data['title']}")
                    
                except Exception as e:
                    print(f"  ⚠️  Error reading {file_path}: {e}")
        
        print(f"  📊 Found {self.stats['stakeholder_docs_found']} stakeholder documents")
    
    def sync_public_docs(self):
        """Sync public documentation - AUTHORITATIVE scan
        
        Finds public documents by:
        - Scanning for markdown files in docs directories
        - Looking for public-facing documentation
        - Checking for README files at various levels
        """
        print("  🔍 Scanning repository for public documentation...")
        
        # Scan entire repository for public documentation
        for root, dirs, files in os.walk(self.repo_root):
            root_path = Path(root)
            
            # Skip excluded directories
            if self._should_skip_dir(root_path):
                dirs[:] = []
                continue
            
            dirs[:] = [d for d in dirs if not (d in self.exclude_dirs or d.startswith('.'))]
            
            for file in files:
                if not file.endswith('.md') or file.startswith('.'):
                    continue
                
                file_path = root_path / file
                
                # Determine if this is a public document
                is_public_doc = False
                path_str = str(file_path.relative_to(self.repo_root)).lower()
                
                # Check for public documentation indicators
                public_keywords = ['docs', 'documentation', 'guide', 'tutorial', 
                                  'readme', 'changelog', 'contributing', 'license',
                                  'launch', 'announcement', 'public']
                
                # Check if in docs directory or has public indicators
                if any(keyword in path_str for keyword in public_keywords):
                    is_public_doc = True
                
                # Exclude internal/stakeholder documents
                internal_keywords = ['stakeholder', 'internal', 'confidential', 
                                    'private', 'restricted']
                if any(keyword in path_str for keyword in internal_keywords):
                    is_public_doc = False
                
                if not is_public_doc:
                    continue
                
                self.stats['docs_found'] += 1
                
                # Read content
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    doc_data = {
                        'title': file_path.stem.replace('-', ' ').replace('_', ' ').title(),
                        'type': self._guess_doc_type(file_path.name),
                        'category': 'Documentation',
                        'content': content[:5000],  # Limit content size
                        'file_path': str(file_path.relative_to(self.repo_root)),
                        'status': 'Published',
                        'published_date': datetime.utcnow().date().isoformat(),
                        'tags': ['public', 'documentation']
                    }
                    
                    # Check if already exists
                    existing = self.db_manager.query('public_db', 'public_documents', 
                                                    {'file_path': doc_data['file_path']})
                    
                    if not existing:
                        self.db_manager.add_record('public_db', 'public_documents', doc_data)
                        self.stats['docs_added'] += 1
                        print(f"  ✓ Added: {doc_data['title']}")
                    
                except Exception as e:
                    print(f"  ⚠️  Error reading {file_path}: {e}")
        
        print(f"  📊 Found {self.stats['docs_found']} public documents")
    
    def _guess_doc_type(self, filename: str) -> str:
        """Guess document type from filename"""
        name_lower = filename.lower()
        
        if 'roadmap' in name_lower:
            return 'Roadmap'
        elif 'report' in name_lower:
            return 'Report'
        elif 'policy' in name_lower:
            return 'Policy'
        elif any(x in name_lower for x in ['readme', 'guide', 'how']):
            return 'Documentation'
        elif any(x in name_lower for x in ['announce', 'launch', 'post']):
            return 'Announcement'
        else:
            return 'Documentation'
    
    def print_stats(self):
        """Print sync statistics"""
        print("=" * 70)
        print("SYNC STATISTICS")
        print("=" * 70)
        print(f"Projects:")
        print(f"  Found: {self.stats['projects_found']}")
        print(f"  Added: {self.stats['projects_added']}")
        print(f"  Updated: {self.stats['projects_updated']}")
        print()
        print(f"Stakeholder Documents:")
        print(f"  Found: {self.stats['stakeholder_docs_found']}")
        print(f"  Added: {self.stats['stakeholder_docs_added']}")
        print()
        print(f"Public Documents:")
        print(f"  Found: {self.stats['docs_found']}")
        print(f"  Added: {self.stats['docs_added']}")
        print()
        print("✅ Sync Complete!")
        print("=" * 70)


def main():
    """Main entry point"""
    # Get repository root
    script_path = Path(__file__).resolve()
    # database/utils/sync_from_repo.py -> utils -> database -> repo_root
    repo_root = script_path.parent.parent.parent
    
    print(f"Repository root: {repo_root}")
    print()
    
    # Create sync instance and run
    sync = RepositorySync(repo_root)
    sync.sync_all()


if __name__ == '__main__':
    main()
