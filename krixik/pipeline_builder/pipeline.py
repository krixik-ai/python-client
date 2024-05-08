import yaml
from typing import Optional, List
from collections import OrderedDict
from krixik.pipeline_builder.module import Module
from krixik.utilities.validators.data.utilities.decorators import datatype_validator
from krixik.utilities.validators.data.utilities.read_config import check_inverse_config
from krixik.pipeline_builder.utilities.config_checker import config_check
from krixik.pipeline_builder.utilities.name_checker import name_check
from krixik.pipeline_builder.utilities.chain_checker import chain_check
from krixik.pipeline_builder.utilities.savepath_checker import savepath_check
from krixik.pipeline_builder.utilities.input_checker import input_check
from krixik.pipeline_builder import MAX_MODULES


def represent_ordereddict(dumper, data):
    return dumper.represent_dict(data.items())


def construct_ordereddict(loader, node):
    return OrderedDict(loader.construct_pairs(node))


yaml.add_representer(OrderedDict, represent_ordereddict)
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_ordereddict)


def convert_to_dict(obj):
    if isinstance(obj, OrderedDict):
        return {key: convert_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    else:
        return obj


class CreatePipeline:
    def __init__(
        self,
        name: Optional[str] = None,
        module_chain: Optional[List[Module]] = None,
        config_path: Optional[str] = None,
    ) -> None:
        self.name = name
        self.__module_chain = []
        self.__module_chain_names = []
        self.__module_chain_output_process_keys = []
        self.__pipeline_config = None
        self.__module_chain_configs = []

        if self.name is not None:
            name_check(self.name)

        if config_path is not None:
            self.load(config_path)

        if module_chain is not None:
            chain_check(module_chain)
            for module in module_chain:
                self._add(module)
            self.test_connections()

    def _add(self, module: Module, insert_index: int = -1) -> None:
        if len(self.__module_chain) + 1 > MAX_MODULES:
            raise ValueError(f"cannot add additional module - pipelines cannot currently have more than {MAX_MODULES} modules")
        if not isinstance(module, Module):
            raise TypeError(f"FAILURE: module - {module} - is not a proper Module object")

        if insert_index != -1:
            if insert_index < -1 or insert_index > len(self.__module_chain):
                raise Exception("insert_index out of range")

            self.__module_chain.insert(insert_index, module)
            self.__module_chain_names.insert(insert_index, module.name)
            self.__module_chain_configs.insert(insert_index, module.config)
            self.__module_chain_output_process_keys.insert(insert_index, module.output_process_key)

        self.__module_chain.append(module)
        self.__module_chain_names.append(module.name)
        self.__module_chain_configs.append(module.config)
        self.__module_chain_output_process_keys.append(module.output_process_key)

        self.test_connections()

    def _remove(
        self,
        module_name: str | None = None,
        index: int | None = None,
    ) -> None:
        if index is not None and (module_name is not None):
            raise Exception("index and module_name cannot both be not None")

        if len(self.__module_chain) == 0:
            raise Exception("no modules to remove")

        # try to find index of module_custom_name in module_chain_custom_names
        if module_name is not None:
            if module_name not in self.__module_chain_names:
                raise Exception(f"module {module_name} not found in pipeline")
        else:
            module_index = self.__module_chain_names.index(module_name)
            self.__module_chain.pop(module_index)
            self.__module_chain_names.pop(module_index)
            self.__module_chain_output_process_keys.pop(module_index)
            self.__module_chain_configs.pop(module_index)

        if index is not None:
            if index < 0 or index >= len(self.__module_chain):
                raise Exception("index out of range")
            self.__module_chain.pop(index)
            self.__module_chain_names.pop(index)
            self.__module_chain_output_process_keys.pop(index)
            self.__module_chain_configs.pop(index)

        # test connections
        self.test_connections()

    @datatype_validator
    def test_input(self, *, local_file_path: str) -> None:
        input_check(local_file_path, self.__module_chain)
        print(f"SUCCESS: local file {local_file_path} passed pipeline input test passed")

    @property
    def module_chain(self) -> list:
        return self.__module_chain_names

    @property
    def module_chain_output_process_keys(self) -> list:
        return self.__module_chain_output_process_keys

    def test_connections(self):
        # if only one module, then no need to check
        if len(self.module_chain) == 1:
            return

        # check if the output_process_key is prev module
        for i in range(len(self.__module_chain) - 1):
            prev_module = self.__module_chain[i]
            prev_module_output_process_key = prev_module.output_process_key
            prev_module_output_process_key_type = prev_module.output_process_type
            prev_module_output_format = prev_module.output_format

            curr_module = self.__module_chain[i + 1]
            curr_module_input_process_key = curr_module.input_process_key
            curr_module_input_process_key_type = curr_module.input_process_type
            curr_module_input_format = curr_module.input_format

            # check format compatibility
            if prev_module_output_format != curr_module_input_format:
                raise TypeError(
                    f"format type mismatch between {prev_module.name} - whose output format is {prev_module_output_format} - and {curr_module.name} - whose input format is {curr_module_input_format}"
                )

            # check process key type compatibility
            if prev_module_output_process_key_type != curr_module_input_process_key_type:
                raise TypeError(
                    f"process key type mismatch between {prev_module.name} - whose output process key is {prev_module_output_process_key} and whose type is {prev_module_output_process_key_type} - and {curr_module.name} - whose input process key {curr_module_input_process_key} whose type is {curr_module_input_process_key_type}"
                )

    def _make_config(self):
        self.__pipeline_config = OrderedDict()
        modules = []
        for ind, mm in enumerate(self.__module_chain_configs):
            module_dict = OrderedDict()
            module = mm["module"]
            module_dict["name"] = module["name"]
            module_dict["models"] = []
            for m in module["models"]:
                entry = {}
                entry["name"] = m["name"]
                if "params" in list(m.keys()):
                    entry["params"] = OrderedDict(m["params"])
                module_dict["models"].append(OrderedDict(entry))

            if "params" in list(module["defaults"].keys()):
                module_dict["defaults"] = OrderedDict({"model": module["defaults"]["model"], "params": OrderedDict(module["defaults"]["params"])})
            else:
                module_dict["defaults"] = OrderedDict({"model": module["defaults"]["model"]})

            module_dict["input"] = OrderedDict(
                {
                    "type": module["input"]["type"],
                    "permitted_extensions": module["input"]["permitted_extensions"],
                }
            )
            module_dict["output"] = OrderedDict({"type": module["output"]["type"]})
            modules.append(module_dict)

        self.__pipeline_config["pipeline"] = OrderedDict({"name": self.name, "modules": modules})

    @property
    def config(self):
        self._make_config()
        return convert_to_dict(self.__pipeline_config)

    def save(self, *, config_path: str) -> None:
        savepath_check(config_path)

        if self.name is None:
            raise ValueError("please give your pipeline a name before saving using the .name property")

        self._make_config()
        with open(config_path, "w") as file:
            yaml.dump(self.__pipeline_config, file, default_flow_style=False, sort_keys=False)

    def load(self, pipeline_config_path: str) -> None:
        config_check(pipeline_config_path)

        with open(pipeline_config_path, "r") as file:
            pipeline_config = yaml.safe_load(file)

        pipeline = pipeline_config["pipeline"]
        pipeline_name = pipeline["name"]
        modules = pipeline["modules"]

        if len(modules) > MAX_MODULES:
            raise ValueError(f"pipelines cannot currently have more than {MAX_MODULES} modules")

        module_chain = []
        for m in modules:
            module_name = m["name"]

            module = Module(
                module_type=module_name,
            )
            module_chain.append(module)

        self.__init__(name=pipeline_name, module_chain=module_chain)
        self._make_config()
