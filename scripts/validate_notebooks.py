#!/usr/bin/env python3
"""
Validate notebooks for common issues and best practices.
"""

import json
import os
import re
import argparse
from pathlib import Path


class NotebookValidator:
    def __init__(self):
        self.issues = []
    
    def validate_notebook(self, notebook_path):
        """Validate a single notebook file."""
        self.issues = []
        
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = json.load(f)
        except json.JSONDecodeError as e:
            self.issues.append(f"Invalid JSON: {e}")
            return self.issues
        except Exception as e:
            self.issues.append(f"Error reading file: {e}")
            return self.issues
        
        self._check_structure(nb)
        self._check_cells(nb)
        self._check_outputs(nb)
        self._check_best_practices(nb)
        
        return self.issues
    
    def _check_structure(self, nb):
        """Check basic notebook structure."""
        if 'cells' not in nb:
            self.issues.append("Missing 'cells' key")
            return
        
        if not isinstance(nb['cells'], list):
            self.issues.append("'cells' should be a list")
        
        if len(nb['cells']) == 0:
            self.issues.append("Notebook has no cells")
    
    def _check_cells(self, nb):
        """Check individual cells."""
        markdown_cells = 0
        code_cells = 0
        
        for i, cell in enumerate(nb.get('cells', [])):
            if 'cell_type' not in cell:
                self.issues.append(f"Cell {i}: Missing cell_type")
                continue
            
            cell_type = cell['cell_type']
            
            if cell_type == 'markdown':
                markdown_cells += 1
                self._check_markdown_cell(cell, i)
            elif cell_type == 'code':
                code_cells += 1
                self._check_code_cell(cell, i)
        
        # Check for reasonable balance
        if code_cells > 0 and markdown_cells == 0:
            self.issues.append("No markdown cells found - consider adding documentation")
    
    def _check_markdown_cell(self, cell, index):
        """Check markdown cell content."""
        source = ''.join(cell.get('source', []))
        
        if not source.strip():
            self.issues.append(f"Cell {index}: Empty markdown cell")
    
    def _check_code_cell(self, cell, index):
        """Check code cell content."""
        source = ''.join(cell.get('source', []))
        
        if not source.strip():
            self.issues.append(f"Cell {index}: Empty code cell")
            return
        
        # Check for common issues
        if 'import' in source and 'from' in source:
            # Check for imports not at the top
            lines = source.split('\n')
            non_import_found = False
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('import') and not line.startswith('from'):
                    non_import_found = True
                elif non_import_found and (line.startswith('import') or line.startswith('from')):
                    self.issues.append(f"Cell {index}: Import statement after other code")
                    break
        
        # Check for hardcoded API keys (basic check)
        if re.search(r'["\'][a-zA-Z0-9]{20,}["\']', source):
            self.issues.append(f"Cell {index}: Possible hardcoded API key or secret")
    
    def _check_outputs(self, nb):
        """Check for outputs that should be cleared."""
        has_outputs = False
        
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'code':
                if cell.get('outputs'):
                    has_outputs = True
                if cell.get('execution_count') is not None:
                    has_outputs = True
        
        if has_outputs:
            self.issues.append("Notebook contains outputs - consider cleaning before commit")
    
    def _check_best_practices(self, nb):
        """Check for best practices."""
        cells = nb.get('cells', [])
        
        if not cells:
            return
        
        # Check if first cell is markdown (good practice)
        if cells[0].get('cell_type') != 'markdown':
            self.issues.append("Consider starting with a markdown cell explaining the notebook")
        
        # Check for very long cells
        for i, cell in enumerate(cells):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if len(source.split('\n')) > 50:
                    self.issues.append(f"Cell {i}: Very long code cell - consider breaking it up")


def validate_notebooks_in_directory(directory):
    """Validate all notebooks in a directory."""
    validator = NotebookValidator()
    results = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                issues = validator.validate_notebook(notebook_path)
                if issues:
                    results[notebook_path] = issues
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Validate Jupyter notebooks')
    parser.add_argument('path', nargs='?', default='notebooks/',
                        help='Path to notebook file or directory (default: notebooks/)')
    parser.add_argument('--strict', action='store_true',
                        help='Exit with error code if any issues found')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path '{path}' does not exist")
        return 1
    
    validator = NotebookValidator()
    
    if path.is_file():
        if not path.suffix == '.ipynb':
            print(f"Error: '{path}' is not a notebook file")
            return 1
        
        issues = validator.validate_notebook(str(path))
        if issues:
            print(f"\n{path}:")
            for issue in issues:
                print(f"  ⚠️  {issue}")
        else:
            print(f"✅ {path}: No issues found")
    else:
        results = validate_notebooks_in_directory(str(path))
        
        if results:
            print("Validation issues found:\n")
            for notebook_path, issues in results.items():
                print(f"{notebook_path}:")
                for issue in issues:
                    print(f"  ⚠️  {issue}")
                print()
        else:
            print("✅ All notebooks passed validation")
    
    if args.strict and (issues if path.is_file() else results):
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())