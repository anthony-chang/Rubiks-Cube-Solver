#!"C:\Users\Anthony Chang\Desktop\UW SE 1A\SE 101\Rubiks-Cube-Solver\Colour-Detection\venv-win\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'pip==19.0.3','console_scripts','pip'
__requires__ = 'pip==19.0.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pip==19.0.3', 'console_scripts', 'pip')()
    )
