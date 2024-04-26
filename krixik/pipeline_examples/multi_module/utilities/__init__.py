multi_module_pipeline_examples = [
    {
        "name": "caption-keyword-search",
        "module_chain": ["caption", "json-to-txt", "keyword-search"],
    },
    {
        "name": "caption-vector-search",
        "module_chain": [
            "caption",
            "json-to-txt",
            "parser",
            "text-embedder",
            "vector-search",
        ],
    },
    {"name": "txt-keyword-search", "module_chain": ["json-to-txt", "keyword-search"]},
    {
        "name": "ocr-vector-search",
        "module_chain": [
            "ocr",
            "json-to-txt",
            "parser",
            "text-embedder",
            "vector-search",
        ],
    },
    {
        "name": "ocr-keyword-search",
        "module_chain": ["ocr", "json-to-txt", "keyword-search"],
    },
    {
        "name": "ocr-sentiment",
        "module_chain": ["ocr", "json-to-txt", "parser", "sentiment"],
    },
    {
        "name": "standard-vector-search",
        "module_chain": ["parser", "text-embedder", "vector-search"],
    },
    {"name": "summarize-sentiment", "module_chain": ["summarize", "sentiment"]},
    {
        "name": "summarize-vector-search",
        "module_chain": [
            "summarize",
            "json-to-txt",
            "parser",
            "text-embedder",
            "vector-search",
        ],
    },
    {
        "name": "summarize-keyword-search",
        "module_chain": ["summarize", "json-to-txt", "keyword-search"],
    },
    {
        "name": "transcribe-vector-search",
        "module_chain": ["transcribe", "text-embedder", "vector-search"],
    },
    {
        "name": "transcribe-keyword-search",
        "module_chain": ["transcribe", "json-to-txt", "keyword-search"],
    },
    {
        "name": "transcribe-translate-vector-search",
        "module_chain": ["transcribe", "translate", "text-embedder", "vector-search"],
    },
    {"name": "transcribe-summarize", "module_chain": ["transcribe", "json-to-txt", "summarize"]},
    {"name": "transcribe-sentiment", "module_chain": ["transcribe", "sentiment"]},
    {
        "name": "translate-vector-search",
        "module_chain": ["translate", "text-embedder", "vector-search"],
    },
    {
        "name": "translate-keyword-search",
        "module_chain": ["translate", "json-to-txt", "keyword-search"],
    },
]
