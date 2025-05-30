Multi-Task-AI-Assistant/
│
├── #file:KI_Training/
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   │   ├── sample_documents/
│   │   │   ├── sample.pdf
│   │   │   ├── sample.docx
│   │   │   ├── sample.txt
│   │   │   └── sample.md
│   │   └── sample_images/
│   │       ├── image1.jpg
│   │       └── image2.png
│   │   └── sample_videos/
│   │       └── video1.mp4
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── wiki_reader.py
│   │   ├── document_reader.py
│   │   ├── image_analyzer.py
│   │   ├── video_analyzer.py
│   │   └── translator.py
│   ├── tests/
│   │   ├── test_wiki_reader.py
│   │   ├── test_document_reader.py
│   │   ├── test_image_analyzer.py
│   │   ├── test_video_analyzer.py
│   │   └── test_translator.py
│   └── notebooks/
│       ├── exploratory_analysis.ipynb
│       └── model_training.ipynb
│
└── .gitignore