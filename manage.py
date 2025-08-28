#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mockshop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Automatically use 127.0.0.1:8080 if no runserver args provided
    if len(sys.argv) == 1:
        sys.argv += ['runserver', '127.0.0.1:8080']

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    import sys
    # Force runserver on 127.0.0.1:8080 always
    for i, arg in enumerate(sys.argv):
        if arg == 'runserver':
            sys.argv[i] = 'runserver'
            if len(sys.argv) <= i + 1 or ':' not in sys.argv[i+1]:
                sys.argv.insert(i+1, '127.0.0.1:8080')
            else:
                sys.argv[i+1] = '127.0.0.1:8080'
    main()

