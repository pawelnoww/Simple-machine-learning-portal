from src.utils.solutionutils import get_solution_dir
from flask_login import current_user
import yaml


def load_config(dst):
    path = f'{dst}/config.yaml'
    file = open(path)
    config = yaml.load(file, Loader=yaml.Loader)
    file.close()
    return config
