import importlib
from krixik.modules import available_modules


def validate_module_selection(module_name: str, module_selections: dict) -> None:
    import_statement = f"krixik.modules.{module_name}.models"
    validator = importlib.import_module(import_statement)
    return validator.model_selection_setup(module_selections).get_setup_result()


def pipeline_selection_setup(
    pipeline_ordered_modules: list, module_selections: dict
) -> dict:
    # check that pipeline_ordered_modules is a list
    if not isinstance(pipeline_ordered_modules, list):
        raise ValueError("pipeline_ordered_modules must be a list")

    # check that module_selections is a dictionary
    if not isinstance(module_selections, dict):
        raise ValueError("module_selections must be a dictionary")

    # check that all keys in module_selections are in pipeline_ordered_modules
    for key in module_selections.keys():
        if key not in pipeline_ordered_modules:
            raise ValueError(
                f"module_selections module - {key} -  not in pipeline_ordered_modules - {key}"
            )

    # check that all keys in module_selections are in available_modules
    for key in module_selections.keys():
        if key not in available_modules:
            raise ValueError(
                f"module_selections module - {key} - not a currently available module - {available_modules}"
            )

    # check each module_selection in module_selections
    hydrated_pipeline_selections = {}
    for module_name in pipeline_ordered_modules:
        if module_name in list(module_selections.keys()):
            module_params = module_selections[module_name]
        else:
            module_params = {}
        hydrated_module_selections = validate_module_selection(
            module_name, module_params
        )
        hydrated_pipeline_selections[module_name] = hydrated_module_selections
    return hydrated_pipeline_selections
