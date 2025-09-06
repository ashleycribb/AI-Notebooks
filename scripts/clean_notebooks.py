#!/usr/bin/env python3
"""
Clean notebooks by removing outputs and execution counts.
This script helps maintain clean notebooks in version control.
"""

import json
import os
import argparse
from pathlib import Path


def clean_notebook(notebook_path):
    """
    Remove outputs and execution counts from a notebook.
    
    Args:
        notebook_path (str): Path to the notebook file
        
    Returns:
        tuple: (notebook_data, changes_made)
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    changes_made = False
    
    for cell in nb.get('cells', []):
        # Clear outputs
        if 'outputs' in cell and cell['outputs']:
            cell['outputs'] = []
            changes_made = True
        
        # Clear execution count
        if 'execution_count' in cell and cell['execution_count'] is not None:
            cell['execution_count'] = None
            changes_made = True
    
    # Clear notebook-level execution count
    if 'execution_count' in nb:
        del nb['execution_count']
        changes_made = True
    
    return nb, changes_made


def clean_notebooks_in_directory(directory, dry_run=False):
    """
    Clean all notebooks in a directory recursively.
    
    Args:
        directory (str): Directory to search for notebooks
        dry_run (bool): If True, don't actually modify files
        
    Returns:
        int: Number of notebooks cleaned
    """
    cleaned_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                nb, changes_made = clean_notebook(notebook_path)
                
                if changes_made:
                    if dry_run:
                        print(f"Would clean: {notebook_path}")
                    else:
                        with open(notebook_path, 'w', encoding='utf-8') as f:
                            json.dump(nb, f, indent=2, ensure_ascii=False)
                        print(f"Cleaned: {notebook_path}")
                    cleaned_count += 1
                else:
                    print(f"Already clean: {notebook_path}")
    
    return cleaned_count


def main():
    parser = argparse.ArgumentParser(description='Clean Jupyter notebooks')
    parser.add_argument('path', nargs='?', default='notebooks/',
                        help='Path to notebook file or directory (default: notebooks/)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be cleaned without making changes')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path '{path}' does not exist")
        return 1
    
    if path.is_file():
        if not path.suffix == '.ipynb':
            print(f"Error: '{path}' is not a notebook file")
            return 1
        
        nb, changes_made = clean_notebook(str(path))
        if changes_made:
            if args.dry_run:
                print(f"Would clean: {path}")
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(nb, f, indent=2, ensure_ascii=False)
                print(f"Cleaned: {path}")
        else:
            print(f"Already clean: {path}")
    else:
        cleaned_count = clean_notebooks_in_directory(str(path), args.dry_run)
        action = "Would clean" if args.dry_run else "Cleaned"
        print(f"\n{action} {cleaned_count} notebooks")
    
    return 0


if __name__ == '__main__':
    exit(main())