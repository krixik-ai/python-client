from krixik.__base__ import library_base_dir
from pathlib import Path
from krixik.modules.utilities.read_config import (
    get_module_available_defaults,
)

module_path_name = Path(__file__).parent.name
module_config_path = library_base_dir + f"/modules/{module_path_name}/module.yml"
module_config = get_module_available_defaults(module_config_path)
