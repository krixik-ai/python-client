multi_module_pipeline_examples = [
    {
        "name": "caption-keyword-db",
        "module_chain": ["caption", "json-to-txt", "keyword-db"],
    },
    {
        "name": "caption-vector-db",
        "module_chain": [
            "caption",
            "json-to-txt",
            "parser",
            "text-embedder",
            "vector-db",
        ],
    },
    {"name": "txt-keyword-db", "module_chain": ["json-to-txt", "keyword-db"]},
    {
        "name": "ocr-vector-db",
        "module_chain": [
            "ocr",
            "json-to-txt",
            "parser",
            "text-embedder",
            "vector-db",
        ],
    },
    {
        "name": "ocr-keyword-db",
        "module_chain": ["ocr", "json-to-txt", "keyword-db"],
    },
    {
        "name": "ocr-sentiment",
        "module_chain": ["ocr", "json-to-txt", "parser", "sentiment"],
    },
    {
        "name": "standard-vector-db",
        "module_chain": ["parser", "text-embedder", "vector-db"],
    },
    {"name": "summarize-sentiment", "module_chain": ["summarize", "sentiment"]},
    {
        "name": "summarize-vector-db",
        "module_chain": [
            "summarize",
            "json-to-txt",
            "parser",
            "text-embedder",
            "vector-db",
        ],
    },
    {
        "name": "summarize-keyword-db",
        "module_chain": ["summarize", "json-to-txt", "keyword-db"],
    },
    {
        "name": "transcribe-vector-db",
        "module_chain": ["transcribe", "text-embedder", "vector-db"],
    },
    {
        "name": "transcribe-keyword-db",
        "module_chain": ["transcribe", "json-to-txt", "keyword-db"],
    },
    {
        "name": "transcribe-translate-vector-db",
        "module_chain": ["transcribe", "translate", "text-embedder", "vector-db"],
    },
    {"name": "transcribe-summarize", "module_chain": ["transcribe", "json-to-txt", "summarize"]},
    {"name": "transcribe-sentiment", "module_chain": ["transcribe", "sentiment"]},
    {
        "name": "translate-vector-db",
        "module_chain": ["translate", "text-embedder", "vector-db"],
    },
    {
        "name": "translate-keyword-db",
        "module_chain": ["translate", "json-to-txt", "keyword-db"],
    },
]
