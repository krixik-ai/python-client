from typing import Optional
from krixik.__version__ import __version__
import tempfile
import types
from krixik.utilities.utilities import classproperty
from krixik.modules import available_modules, get_module_details
from krixik.system_builder.functions.checkin import checkin
from krixik.pipeline_builder.pipeline import CreatePipeline
from krixik.system_builder.base import KrixikBasePipeline
from krixik.system_builder.functions.semantic_search import semantic_search
from krixik.system_builder.functions.keyword_search import keyword_search
from krixik.pipeline_builder.utilities.config_checker import config_check
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline


class krixik:
    """Main class for krixik pipeline selection and initialization"""

    __api_key = None
    __api_url = None
    __api_check_val = None
    __local_conversion_directory = tempfile.gettempdir()

    @classmethod
    def init(cls, *, api_key: str | None, api_url: str | None) -> None:
        """krixik pipeline initialization method - initializes unique user session using api_key and api_url

        Parameters
        ----------
        api_key : str
            user api key
        api_url : str
            user api url
        """
        cls.__api_key = api_key
        cls.__api_url = api_url
        cls.__api_check_val = checkin(cls.__api_key, cls.__api_url)
        cls.__version = __version__

    @classmethod
    def check_init_data(cls) -> dict:
        """convenience check for init of api_key and api_url

        Returns
        -------
        dict
            dictionary with api_key, api_url and api_check_val
        """
        return {
            "api_key": cls.__api_key,
            "api_url": cls.__api_url,
            "api_check_val": cls.__api_check_val,
        }

    @classmethod
    def create_pipeline(cls, *, name: str, module_chain: list):
        if not isinstance(name, str):
            raise TypeError("pipeline name must be a string")
        if not (len(name) > 0 and len(name) < 128):
            raise ValueError("pipeline name must have length greater than 0 and less than 128")
        if not isinstance(module_chain, list):
            raise TypeError("module_chain must be a list of strings")
        for item in module_chain:
            if not isinstance(item, str):
                raise TypeError(f"module_chain must be a list of strings - the following item in it is not a string - {item}")
            if item not in available_modules:
                raise ValueError(f"module_chain item - {item} - is not a currently one of the currently available modules -{available_modules}")
        module_chain_ = [Module(m_name) for m_name in module_chain]
        custom = CreatePipeline(name=name, module_chain=module_chain_)
        return cls.load_pipeline(pipeline=custom)

    @classmethod
    def load_pipeline(cls, *, config_path: Optional[str] = None, pipeline: Optional[CreatePipeline] = None) -> object:
        """load pipeline: from object or configuration file

        Parameters
        ----------
        config_path : str
            path to pipeline configuration file
        pipeline: CreatePipeline
            pipeline object
        """
        # only one of config_path or pipeline can be passed
        if config_path is None and pipeline is None:
            raise ValueError("config_path or pipeline must be passed")

        if config_path is not None and pipeline is not None:
            raise ValueError("only one of config_path or pipeline can be passed, not both")

        if config_path is not None:
            config_check(config_path)
            custom_pipeline = CreatePipeline(config_path=config_path)
        else:
            if not isinstance(pipeline, CreatePipeline):
                raise TypeError(f"pipeline - {pipeline} not proper CreatePipeline object")
            custom_pipeline = pipeline

        # pass init
        init_data = cls.check_init_data()

        # instantiate krixik server pipeline object
        pipeline_object = KrixikBasePipeline(
            pipeline=custom_pipeline.name,
            module_chain=custom_pipeline.module_chain,
            output_process_keys=custom_pipeline.module_chain_output_process_keys,
            api_key=init_data["api_key"],
            api_url=init_data["api_url"],
            api_check_val=init_data["api_check_val"],
        )

        pipeline_object.save_pipeline = custom_pipeline.save
        pipeline_object.test_input = custom_pipeline.test_input
        pipeline_object.config = custom_pipeline.config

        if custom_pipeline.module_chain[-1] == "vector-db":
            if len(custom_pipeline.module_chain) > 1:
                if custom_pipeline.module_chain[-2] == "text-embedder":
                    pipeline_object.semantic_search = types.MethodType(semantic_search, pipeline_object)

        if custom_pipeline.module_chain[-1] == "keyword-db":
            pipeline_object.keyword_search = types.MethodType(keyword_search, pipeline_object)

        return pipeline_object

    @classmethod
    def view_module_config(cls, *, module_name: str) -> dict:
        """convenience method for examinng module details

        Parameters
        ----------
        module_name : str
            module name

        Returns
        -------
        dict
            dictionary with module details
        """
        return get_module_details(module_name)

    @classmethod
    def view_module_click_data(cls, *, module_name: str) -> dict:
        return Module(module_name).click_data

    @classproperty
    def local_conversion_directory(cls):
        return cls.__local_conversion_directory

    @classproperty
    def available_modules(cls):
        return available_modules

    @classproperty
    def version(cls):
        return cls.__version

    def __getattr__(self, attr):
        raise AttributeError(f"'{self.__class__.__name__}' object instance has no attribute '{attr}'")
