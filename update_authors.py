#!/usr/bin/env python3
"""
Script to update author and ms.author fields in Azure Machine Learning documentation.

This script processes all markdown files in the articles/machine-learning directory
and its subdirectories, updating author metadata fields according to specified mappings.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def load_mappings() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Load the author and ms.author mappings.
    
    Returns:
        Tuple of (author_mappings, ms_author_mappings)
    """
    # Author field mappings (case-insensitive input, lowercase output)
    author_mappings = {
        'blackmist': 's-polly',
        'sdgilley': 's-polly', 
        'lgayhardt': 's-polly',
        'ssalgadodev': 's-polly',
        'fbsolo-ms1': 's-polly',
        'msakande': 's-polly'
    }
    
    # Ms.author field mappings (case-insensitive input, lowercase output)  
    ms_author_mappings = {
        'larryfr': 'scottpolly',
        'sgilley': 'scottpolly',
        'lagayhar': 'scottpolly', 
        'ssalgado': 'scottpolly',
        'franksolomon': 'scottpolly',
        'mopeakande': 'scottpolly'
    }
    
    return author_mappings, ms_author_mappings


def process_markdown_file(file_path: Path, author_mappings: Dict[str, str], 
                         ms_author_mappings: Dict[str, str]) -> Tuple[bool, List[str]]:
    """
    Process a single markdown file to update author fields.
    
    Args:
        file_path: Path to the markdown file
        author_mappings: Dictionary mapping old author values to new ones
        ms_author_mappings: Dictionary mapping old ms.author values to new ones
        
    Returns:
        Tuple of (was_modified, list_of_changes)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False, []
    
    original_content = content
    changes = []
    
    # Process author field
    # Pattern matches: author: value (with optional spaces and trailing spaces)
    author_pattern = r'^(\s*author:\s*)([^\r\n]+?)(\s*)$'
    
    def replace_author(match):
        prefix = match.group(1)
        author_value = match.group(2).strip()
        suffix = match.group(3)
        
        # Check if this author should be updated (case-insensitive)
        author_lower = author_value.lower()
        if author_lower in author_mappings:
            new_author = author_mappings[author_lower]
            changes.append(f"author: {author_value} -> {new_author}")
            return f"{prefix}{new_author}{suffix}"
        
        return match.group(0)  # No change
    
    content = re.sub(author_pattern, replace_author, content, flags=re.MULTILINE)
    
    # Process ms.author field  
    # Pattern matches: ms.author: value (with optional spaces and trailing spaces)
    ms_author_pattern = r'^(\s*ms\.author:\s*)([^\r\n]+?)(\s*)$'
    
    def replace_ms_author(match):
        prefix = match.group(1)
        ms_author_value = match.group(2).strip()
        suffix = match.group(3)
        
        # Check if this ms.author should be updated (case-insensitive)
        ms_author_lower = ms_author_value.lower()
        if ms_author_lower in ms_author_mappings:
            new_ms_author = ms_author_mappings[ms_author_lower]
            changes.append(f"ms.author: {ms_author_value} -> {new_ms_author}")
            return f"{prefix}{new_ms_author}{suffix}"
        
        return match.group(0)  # No change
    
    content = re.sub(ms_author_pattern, replace_ms_author, content, flags=re.MULTILINE)
    
    # Write back if content changed
    was_modified = content != original_content
    if was_modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False, []
    
    return was_modified, changes


def find_markdown_files(base_path: Path) -> List[Path]:
    """
    Find all markdown files in the articles/machine-learning directory and subdirectories.
    
    Args:
        base_path: Base directory path
        
    Returns:
        List of markdown file paths
    """
    ml_path = base_path / "articles" / "machine-learning" 
    
    if not ml_path.exists():
        print(f"Error: Directory {ml_path} does not exist")
        return []
    
    markdown_files = list(ml_path.glob("**/*.md"))
    return markdown_files


def main():
    """Main function to process all markdown files."""
    
    # Get the script directory and assume it's in the repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir
    
    print(f"Processing markdown files in {repo_root / 'articles' / 'machine-learning'}")
    
    # Load mappings
    author_mappings, ms_author_mappings = load_mappings()
    
    print("Author mappings:")
    for old, new in author_mappings.items():
        print(f"  {old} -> {new}")
    
    print("\nMs.author mappings:")
    for old, new in ms_author_mappings.items():
        print(f"  {old} -> {new}")
    
    print("\n" + "="*60)
    
    # Find all markdown files
    markdown_files = find_markdown_files(repo_root)
    
    if not markdown_files:
        print("No markdown files found.")
        return
    
    print(f"Found {len(markdown_files)} markdown files to process.\n")
    
    # Process each file
    total_modified = 0
    total_changes = 0
    
    for file_path in markdown_files:
        was_modified, changes = process_markdown_file(file_path, author_mappings, ms_author_mappings)
        
        if was_modified:
            total_modified += 1
            total_changes += len(changes)
            
            # Show relative path for cleaner output
            rel_path = file_path.relative_to(repo_root)
            print(f"Modified: {rel_path}")
            for change in changes:
                print(f"  - {change}")
            print()
    
    print("="*60)
    print(f"Summary:")
    print(f"  Files processed: {len(markdown_files)}")
    print(f"  Files modified: {total_modified}")
    print(f"  Total changes made: {total_changes}")
    
    if total_modified == 0:
        print("\nNo files needed to be modified.")
    else:
        print(f"\nSuccessfully updated {total_modified} files with {total_changes} changes.")


if __name__ == "__main__":
    main()
