#!"C:\Users\Aragon Perez\Documents\Estructura de Datos\EDD_2S2019_P2_201701133\[EDD]P2_201701133\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'pip==19.0.3','console_scripts','pip3.7'
__requires__ = 'pip==19.0.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pip==19.0.3', 'console_scripts', 'pip3.7')()
    )
