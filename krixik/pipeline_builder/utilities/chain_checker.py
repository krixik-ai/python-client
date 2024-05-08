from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder import MAX_MODULES


def chain_check(module_chain: list) -> None:
    if not isinstance(module_chain, list):
        raise TypeError(f"FAILURE: module_chain - {module_chain} - is not a list")
    if len(module_chain) == 0:
        raise ValueError(f"FAIULRE: module_chain - {module_chain} is empty")
    for item in module_chain:
        if not isinstance(item, Module):
            raise TypeError(f"FAILURE: item in module_chain - {item} - is not a proper Module object")

    if len(module_chain) > MAX_MODULES:
        raise ValueError(f"pipelines cannot currently have more than {MAX_MODULES} modules")
