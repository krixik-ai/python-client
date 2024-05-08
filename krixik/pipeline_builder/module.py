from regex import P
import yaml
from krixik.__base__ import library_base_dir
import importlib
from krixik.modules import available_modules
from krixik.utilities.validators.data.utilities.read_config import get_allowable_data_types


class Module:
    def __init__(self, module_type: str) -> None:
        if not isinstance(module_type, str):
            raise ValueError("module_type must be a string")

        self.name = module_type

        # check validity of input module
        if self.name not in available_modules:
            raise Exception(f"user defined module {self.name} does not exist")

        # define config and io paths
        self.__module_config_path = library_base_dir + f"/modules/{self.name}/module.yml"
        self.__io_module_path = f"krixik.modules.{self.name}.io"

        # load in module config
        self.__module_config = None
        if self.name is not None:
            with open(self.__module_config_path, "r") as file:
                self.__module_config = yaml.safe_load(file)
        else:
            raise Exception(f"please select a valid module from the available options: {available_modules}")
        # attach permitted extensions to module config
        self.__module_config["module"]["input"]["permitted_extensions"] = get_allowable_data_types(self.__module_config["module"]["input"]["type"])
        self.__module_config["module"]["output"]["permitted_extensions"] = get_allowable_data_types(self.__module_config["module"]["output"]["type"])

        io_module = importlib.import_module(self.__io_module_path)
        self.__input_dataclass = io_module.InputStructure if hasattr(io_module, "InputStructure") else None
        if self.__input_dataclass is None:
            raise Exception(f"error loading in {self.name} io module {self.__io_module_path} - InputStructure not found")

        self.__input_structure = self.__input_dataclass().__dict__
        self.__input_example = self.__input_dataclass().data_example
        self.__input_format = self.__input_dataclass().format
        self.__input_process_key = self.__input_dataclass().process_key
        self.__input_process_type = self.__input_dataclass().process_type

        self.__output_dataclass = io_module.OutputStructure if hasattr(io_module, "OutputStructure") else None
        if self.__output_dataclass is None:
            raise Exception(f"error loading in {self.name} io module {self.__io_module_path} - OutputStructure not found")

        self.__output_structure = self.__output_dataclass().__dict__
        self.__output_example = self.__output_dataclass().data_example
        self.__output_format = self.__output_dataclass().format
        self.__output_process_key = self.__output_dataclass().process_key
        self.__output_process_type = self.__output_dataclass().process_type

    @property
    def config(self):
        return self.__module_config

    @property
    def input_structure(self):
        return self.__input_structure

    @property
    def output_structure(self):
        return self.__output_structure

    @property
    def input_format(self):
        return self.__input_format

    @property
    def output_format(self):
        return self.__output_format

    @property
    def input_example(self):
        return self.__input_example

    @property
    def output_example(self):
        return self.__output_example

    @property
    def input_process_key(self):
        return self.__input_process_key

    @property
    def output_process_key(self):
        return self.__output_process_key

    @property
    def input_process_type(self):
        return self.__input_process_type

    @property
    def output_process_type(self):
        return self.__output_process_type

    @property
    def click_data(self):
        return {
            "module_name": self.name,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "input_process_key": self.input_process_key,
            "input_process_type": self.input_process_type,
            "output_process_key": self.output_process_key,
            "output_process_type": self.output_process_type,
        }
