def clean_strings(input_data: str | list):
    if input_data is not None:
        if isinstance(input_data, str):
            c_string = input_data.replace("\n", " ").replace("\r", "").strip()
            return c_string
        elif isinstance(input_data, list):
            c_strings = [v.replace("\n", " ").replace("\r", "").strip() for v in input_data]
            return c_strings
