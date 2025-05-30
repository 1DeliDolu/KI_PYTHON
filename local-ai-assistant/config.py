"""
Configuration settings for Multi-Task AI Assistant
"""

import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Config:
    """Configuration class for the AI Assistant"""
    
    # Application settings
    APP_NAME: str = "Multi-Task AI Assistant"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Directories
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    TEMP_DIR: str = os.path.join(BASE_DIR, "temp")
    
    # Wikipedia settings
    WIKIPEDIA_LANGUAGE: str = "en"
    WIKIPEDIA_MAX_RESULTS: int = 3
    WIKIPEDIA_AUTO_SUGGEST: bool = True
    
    # Document reader settings
    SUPPORTED_DOC_FORMATS: list = None
    MAX_FILE_SIZE_MB: int = 50
    
    # Image analysis settings
    SUPPORTED_IMAGE_FORMATS: list = None
    IMAGE_MAX_SIZE_MB: int = 20
    
    # Video analysis settings
    SUPPORTED_VIDEO_FORMATS: list = None
    VIDEO_MAX_SIZE_MB: int = 100
    VIDEO_FRAME_EXTRACT_INTERVAL: int = 30  # seconds
    
    # Translation settings
    DEFAULT_SOURCE_LANG: str = "auto"
    DEFAULT_TARGET_LANG: str = "en"
    TRANSLATION_SERVICE: str = "googletrans"  # or "azure", "openai"
    
    # Model settings
    USE_GPU: bool = False
    MODEL_CACHE_DIR: str = os.path.join(MODELS_DIR, "cache")
    
    # API Keys (to be set via environment variables)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    AZURE_TRANSLATOR_KEY: str = os.getenv("AZURE_TRANSLATOR_KEY", "")
    AZURE_TRANSLATOR_REGION: str = os.getenv("AZURE_TRANSLATOR_REGION", "")
    
    def __post_init__(self):
        """Initialize default values after object creation"""
        if self.SUPPORTED_DOC_FORMATS is None:
            self.SUPPORTED_DOC_FORMATS = ['.txt', '.pdf', '.docx', '.doc', '.rtf']
        
        if self.SUPPORTED_IMAGE_FORMATS is None:
            self.SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        
        if self.SUPPORTED_VIDEO_FORMATS is None:
            self.SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            self.DATA_DIR,
            self.MODELS_DIR,
            self.TEMP_DIR,
            self.MODEL_CACHE_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
    
    def update_config(self, **kwargs):
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")
    
    def is_file_supported(self, file_path: str, file_type: str) -> bool:
        """Check if file format is supported"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_type == "document":
            return file_ext in self.SUPPORTED_DOC_FORMATS
        elif file_type == "image":
            return file_ext in self.SUPPORTED_IMAGE_FORMATS
        elif file_type == "video":
            return file_ext in self.SUPPORTED_VIDEO_FORMATS
        else:
            return False
    
    def get_file_size_mb(self, file_path: str) -> float:
        """Get file size in MB"""
        if os.path.exists(file_path):
            return os.path.getsize(file_path) / (1024 * 1024)
        return 0
    
    def validate_file(self, file_path: str, file_type: str) -> tuple[bool, str]:
        """Validate file based on type and size"""
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        if not self.is_file_supported(file_path, file_type):
            return False, f"Unsupported {file_type} format"
        
        file_size = self.get_file_size_mb(file_path)
        
        max_size = {
            "document": self.MAX_FILE_SIZE_MB,
            "image": self.IMAGE_MAX_SIZE_MB,
            "video": self.VIDEO_MAX_SIZE_MB
        }.get(file_type, self.MAX_FILE_SIZE_MB)
        
        if file_size > max_size:
            return False, f"File size ({file_size:.1f}MB) exceeds maximum allowed size ({max_size}MB)"
        
        return True, "File is valid"