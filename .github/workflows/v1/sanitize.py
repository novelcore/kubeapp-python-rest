import re
import os
import sys

def sanitize_name(name, max_length=30):
    if not name:
        raise ValueError("Name cannot be empty")
    
    # Convert to lowercase first
    sanitized = name.lower()
    
    # Replace common special characters with more specific replacements
    replacements = {
        '@': 'at',
        '&': 'and',
        '+': 'plus',
        '$': 's',
        '_': '-',
        '.': '-',
        '/': '-',
        '\\': '-',
        ' ': '-'
    }
    for char, replacement in replacements.items():
        sanitized = sanitized.replace(char, replacement)
    
    # Remove all other non-alphanumeric characters except hyphen
    sanitized = re.sub(r'[^a-z0-9\-]', '', sanitized)
    
    # Replace multiple consecutive hyphens with a single hyphen
    sanitized = re.sub(r'-+', '-', sanitized)
    
    # Remove hyphens from start and end
    sanitized = sanitized.strip('-')
    
    # Ensure the name starts with an alphanumeric character
    sanitized = re.sub(r'^[^a-z0-9]+', '', sanitized)
    
    # Ensure the name ends with an alphanumeric character
    sanitized = re.sub(r'[^a-z0-9]+$', '', sanitized)
    
    # Truncate to max length while ensuring we don't end with a hyphen
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        # If we happen to end with a hyphen after truncating, remove it
        sanitized = sanitized.rstrip('-')
    
    # Final validation
    if not sanitized:
        raise ValueError("Sanitization resulted in an empty string")
    
    if not re.match(r'^[a-z0-9][a-z0-9\-]*[a-z0-9]$', sanitized):
        raise ValueError("Failed to create a valid DNS name")
    
    return sanitized

if __name__ == "__main__":
    pr_title = sys.argv[1]
    print(f"Original title: {pr_title}")
    sanitized = sanitize_name(pr_title)
    print(f"Sanitized title: {sanitized}")
    
    # Write to GITHUB_ENV
    with open(os.environ["GITHUB_ENV"], "a") as env_file:
        env_file.write(f"sanitized_pr_title={sanitized}\n")