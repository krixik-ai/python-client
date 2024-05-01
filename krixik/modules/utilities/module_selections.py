import importlib
from collections import Counter
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
    
    # check that entries of pipeline_ordered_modules are strings
    for entry in pipeline_ordered_modules:
        if not isinstance(entry, str):
            raise TypeError("all entries of pipeline_ordered_modules must be strings")

    # check that module_selections is a dictionary
    if not isinstance(module_selections, dict):
        raise TypeError("module_selections must be a dictionary")
    
    module_selection_names = list(module_selections.keys())
    
    # check that each value of module_selections is a dict
    for key in module_selection_names:
        if not isinstance(module_selections[key], dict):
            raise TypeError("each value of module_selections must be a dict")
        
    # check that there are not more module_selections than there are modules in pipeline
    if len(module_selection_names) > len(pipeline_ordered_modules):
        raise ValueError(f"you have entered {len(module_selection_names)} module configurations but your pipeline contains only {len(pipeline_ordered_modules)} modules")

    # make sure not multiple selection labels
    select_counts = Counter(module_selection_names)
    select_has_dups = any(count > 1 for count in select_counts.values())
    if select_has_dups:
        raise ValueError(f"your module selection labels cannot contain duplicate entries - {module_selection_names}")

    # switch for forced use module_i notation in module_selection on duplicate module use
    pipeilne_counts = Counter(pipeline_ordered_modules)
    pipeline_has_dups = any(count > 1 for count in pipeilne_counts.values())
    module_i_labels = [f"module_{i}" for i in range(1, len(pipeline_ordered_modules)+1)]

    select_contains_index_label = any(item.startswith("module_") for item in module_selection_names)
    
    STOPPED HERE - address below
    
    available_selection_labels = available_modules + module_i_labels

    # check that all keys in module_selections are in pipeline_ordered_modules or module_i format
    for key in module_selections.keys():
        if pipeline_has_dups:
            if key not in module_i_labels:
                raise ValueError(f"when using duplicate modules your module selection labels must lie in the index set: {module_i_labels} so that your model/param selections can be correctly mapped to the proper modules")
        else:
            if key not in available_selection_labels:
                raise ValueError(
                    f"module_selections module - {key} -  not in pipeline_ordered_modules - {pipeline_ordered_modules} - or in optional index set labels: {module_i_labels}"
                )
                
    # check that all keys in module_selections are in available_modules
    for key in module_selections.keys():
        if key not in available_selection_labels:
            raise ValueError(
                f"module_selections module - {key} - not a currently available module - {available_modules} - or in optional index set - {module_i_labels}"
            )

    # check for model/param configuration for each module in pipeline
    hydrated_pipeline_selections = {}
    module_select_names = list(module_selections.keys())
    for module_name in pipeline_ordered_modules:    
        if module_name in module_select_names:
            module_params = module_selections[module_name]
        if module_name[:7] == "module_":
            pipeline_index = int(module_name.split("_")[1])
            
        
        else:
            module_params = {}
        hydrated_module_selections = validate_module_selection(
            module_name, module_params
        )
        hydrated_pipeline_selections[module_name] = hydrated_module_selections
    return hydrated_pipeline_selections
