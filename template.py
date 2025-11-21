import logging
import os


from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    'src/__init__.py',
    'setup.py',
    '.gitignore',
    'app.py',
    '.env',
    'src/config/__init__.py',
    'src/config/config.py',
    'requirements.txt',
    'app/__init__.py',
    'app/backend/data',
    'app/frontend/data',
    'app/common/__init__.py',
    'app/common/logger.py',
    'app/common/custom_exception.py',
    'app/core/data',
    'app/config/data',
    'app/main.py'

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f'Creating directory: {filedir} for the file {filename}')

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f'Creating empth file: {filepath}')
    else:
        logging.info(f'{filename} already exists')
