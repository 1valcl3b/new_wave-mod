from pathlib import Path

PATH_ROOT = Path(__file__).resolve().parent.parent

ENV_PATH = PATH_ROOT / '.env'

PATH_APP = PATH_ROOT / 'app'

config_dir = PATH_APP / 'provision'