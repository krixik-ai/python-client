from typing import Optional
from krixik.__version__ import __version__
import tempfile
import types

from krixik.utilities.utilities import classproperty

from krixik.modules import available_modules, get_module_details

from krixik.system_builder.functions.checkin import checkin

from krixik.pipeline_builder.pipeline import CreatePipeline
from krixik.system_builder.base import KrixikBasePipeline
from krixik.system_builder.functions.vector_search import vector_search
from krixik.system_builder.functions.keyword_search import keyword_search


class krixik:
    """Main class for krixik pipeline selection and initialization"""

    __api_key = None
    __api_url = None
    __api_check_val = None
    __local_conversion_directory = tempfile.gettempdir()

    @classmethod
    def init(cls, api_key: str | None, api_url: str | None) -> None:
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
    def load_pipeline(cls,
                      config_path: Optional[str] = None,
                      pipeline: Optional[CreatePipeline] = None
                      ) -> object:
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
            raise ValueError("only one of config_path or pipeline can be passed")
        
        if config_path is not None:
            # instantiate custom pipeline object
            custom_pipeline = CreatePipeline(config_path=config_path)
        else:
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
            api_check_val=init_data["api_check_val"]
        )
                
        pipeline_object.test_input = custom_pipeline.test_input
        
        if custom_pipeline.module_chain[-1] == "vector-db":
            if len(custom_pipeline.module_chain) > 1:
                if custom_pipeline.module_chain[-2] == "text-embedder":
                    pipeline_object.vector_search = types.MethodType(vector_search, pipeline_object)


        if custom_pipeline.module_chain[-1] == "keyword-db":
            pipeline_object.keyword_search = types.MethodType(keyword_search, pipeline_object)
        
        return pipeline_object

    @classmethod
    def module_details(cls, module_name: str) -> dict:
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
        raise AttributeError(
            f"'{self.__class__.__name__}' object instance has no attribute '{attr}'"
        )
