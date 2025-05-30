Multi-Task AI Assistant/
│
├── README.md                     # Project overview and setup instructions
├── requirements.txt              # List of dependencies
├── main.py                       # Main entry point for the application
│
├── wiki_module/                  # Module for Wikipedia querying
│   ├── __init__.py
│   ├── wiki_reader.py            # Functions to read and query Wikipedia
│   └── wiki_utils.py             # Utility functions for Wikipedia interaction
│
├── document_module/              # Module for document reading
│   ├── __init__.py
│   ├── pdf_reader.py             # Functions to read PDF files
│   ├── doc_reader.py             # Functions to read DOC files
│   ├── txt_reader.py             # Functions to read TXT files
│   └── md_reader.py              # Functions to read MD files
│
├── image_module/                 # Module for image analysis
│   ├── __init__.py
│   ├── image_analyzer.py         # Functions for image analysis
│   └── image_utils.py            # Utility functions for image processing
│
├── video_module/                 # Module for video analysis
│   ├── __init__.py
│   ├── video_analyzer.py         # Functions for video analysis
│   └── video_utils.py            # Utility functions for video processing
│
├── translation_module/           # Module for translation
│   ├── __init__.py
│   ├── translator.py              # Functions for translating text
│   └── lang_utils.py             # Utility functions for language processing
│
└── tests/                        # Directory for unit tests
    ├── __init__.py
    ├── test_wiki.py              # Tests for Wikipedia module
    ├── test_document.py          # Tests for document reading module
    ├── test_image.py             # Tests for image analysis module
    ├── test_video.py             # Tests for video analysis module
    └── test_translation.py        # Tests for translation module