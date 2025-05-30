"""
Translation Module
Handles text translation between different languages
"""

import logging
from typing import Dict, List, Optional
from deep_translator import GoogleTranslator as DeepGoogleTranslator
from deep_translator import single_detection
import sys
import os

# Add parent directory to path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class Translator:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        # Language codes mapping
        self.language_codes = {
            'turkish': 'tr', 'türkçe': 'tr', 'tr': 'tr',
            'english': 'en', 'ingilizce': 'en', 'en': 'en',
            'german': 'de', 'almanca': 'de', 'de': 'de',
            'french': 'fr', 'fransızca': 'fr', 'fr': 'fr',
            'spanish': 'es', 'ispanyolca': 'es', 'es': 'es',
            'italian': 'it', 'italyanca': 'it', 'it': 'it',
            'russian': 'ru', 'rusça': 'ru', 'ru': 'ru',
            'chinese': 'zh', 'çince': 'zh', 'zh': 'zh',
            'japanese': 'ja', 'japonca': 'ja', 'ja': 'ja',
            'korean': 'ko', 'korece': 'ko', 'ko': 'ko',
            'arabic': 'ar', 'arapça': 'ar', 'ar': 'ar',
            'portuguese': 'pt', 'portekizce': 'pt', 'pt': 'pt',
            'dutch': 'nl', 'hollandaca': 'nl', 'nl': 'nl',
            'swedish': 'sv', 'isveççe': 'sv', 'sv': 'sv',
            'danish': 'da', 'danca': 'da', 'da': 'da',
            'norwegian': 'no', 'norveççe': 'no', 'no': 'no',
            'polish': 'pl', 'lehçe': 'pl', 'pl': 'pl',
            'czech': 'cs', 'çekçe': 'cs', 'cs': 'cs',
            'hungarian': 'hu', 'macarca': 'hu', 'hu': 'hu',
            'greek': 'el', 'yunanca': 'el', 'el': 'el',
            'hebrew': 'he', 'ibrance': 'he', 'he': 'he',
            'hindi': 'hi', 'hintçe': 'hi', 'hi': 'hi',
            'thai': 'th', 'tayca': 'th', 'th': 'th',
            'vietnamese': 'vi', 'vietnamca': 'vi', 'vi': 'vi'
        }
    
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> Dict:
        """
        Translate text to target language
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code or name
            source_language (str): Source language code (auto-detect if "auto")
            
        Returns:
            Dict: Translation result with metadata
        """
        try:
            if not text or not text.strip():
                return {
                    "success": False,
                    "message": "Empty text provided",
                    "original_text": text,
                    "translated_text": ""
                }
            
            # Normalize language codes
            target_lang = self._normalize_language_code(target_language)
            source_lang = self._normalize_language_code(source_language) if source_language != "auto" else "auto"
            
            if not target_lang:
                return {
                    "success": False,
                    "message": f"Unsupported target language: {target_language}",
                    "original_text": text,
                    "translated_text": ""
                }
              # Try deep-translator directly
            try:
                result = self._translate_with_deep_translator(text, target_lang, source_lang)
                return result
            except Exception as e:
                self.logger.error(f"Translation failed: {e}")
                return {
                    "success": False,
                    "message": f"Translation service failed: {str(e)}",
                    "original_text": text,
                    "translated_text": ""
                }
                
        except Exception as e:
            self.logger.error(f"Error in translation: {e}")
            return {
                "success": False,
                "message": f"Translation error: {str(e)}",
                "original_text": text,
                "translated_text": ""
            }
      def _translate_with_deep_translator(self, text: str, target_lang: str, source_lang: str) -> Dict:
        """Translate using deep-translator library"""
        try:
            if source_lang == "auto":
                # Try to detect language
                try:
                    detected_lang = single_detection(text, api_key=None)
                    source_lang = detected_lang if detected_lang else "en"
                except:
                    source_lang = "en"  # Default fallback
            
            # Create translator instance
            translator = DeepGoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(text)
            
            return {
                "success": True,
                "original_text": text,
                "translated_text": translated_text,
                "source_language": source_lang,
                "target_language": target_lang,
                "confidence": None,
                "service": "deep-translator"
            }
            
        except Exception as e:
            raise Exception(f"Deep translator error: {str(e)}")
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect the language of given text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Detection result with language code and confidence
        """
        try:
            if not text or not text.strip():
                return {
                    "success": False,
                    "message": "Empty text provided",
                    "detected_language": None,
                    "confidence": 0
                }
            
            try:
                detected_lang = single_detection(text, api_key=None)
                return {
                    "success": True,
                    "text": text,
                    "detected_language": detected_lang,
                    "language_name": self._get_language_name(detected_lang),
                    "confidence": 0.8  # Default confidence for deep-translator
                }
            except:
                return {
                    "success": False,
                    "message": "Could not detect language",
                    "detected_language": "en",  # Default fallback
                    "confidence": 0
                }
            
        except Exception as e:
            self.logger.error(f"Error detecting language: {e}")
            return {
                "success": False,
                "message": f"Language detection error: {str(e)}",
                "detected_language": None,
                "confidence": 0
            }
    
    def _get_language_name(self, language_code: str) -> str:
        """Get language name from language code"""
        language_names = {
            'tr': 'Turkish', 'en': 'English', 'de': 'German', 'fr': 'French',
            'es': 'Spanish', 'it': 'Italian', 'ru': 'Russian', 'zh': 'Chinese',
            'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'pt': 'Portuguese',
            'nl': 'Dutch', 'sv': 'Swedish', 'da': 'Danish', 'no': 'Norwegian',
            'pl': 'Polish', 'cs': 'Czech', 'hu': 'Hungarian', 'el': 'Greek',
            'he': 'Hebrew', 'hi': 'Hindi', 'th': 'Thai', 'vi': 'Vietnamese'
        }
        return language_names.get(language_code, language_code.upper())
    
    def translate_batch(self, texts: List[str], target_language: str, source_language: str = "auto") -> Dict:
        """
        Translate multiple texts at once
        
        Args:
            texts (List[str]): List of texts to translate
            target_language (str): Target language code or name
            source_language (str): Source language code (auto-detect if "auto")
            
        Returns:
            Dict: Batch translation results
        """
        try:
            if not texts:
                return {
                    "success": False,
                    "message": "No texts provided",
                    "results": []
                }
            
            results = []
            successful_translations = 0
            
            for i, text in enumerate(texts):
                result = self.translate(text, target_language, source_language)
                results.append({
                    "index": i,
                    "original_text": text,
                    "translation_result": result
                })
                
                if result["success"]:
                    successful_translations += 1
            
            return {
                "success": True,
                "total_texts": len(texts),
                "successful_translations": successful_translations,
                "failed_translations": len(texts) - successful_translations,
                "target_language": target_language,
                "source_language": source_language,
                "results": results
            }
            
        except Exception as e:
            self.logger.error(f"Error in batch translation: {e}")
            return {
                "success": False,
                "message": f"Batch translation error: {str(e)}",
                "results": []
            }
    
    def get_supported_languages(self) -> Dict:
        """Get list of supported languages"""
        return {
            "success": True,
            "supported_languages": self.language_codes,
            "language_count": len(self.language_codes)
        }
    
    def translate_file(self, file_path: str, target_language: str, output_path: str, source_language: str = "auto") -> Dict:
        """
        Translate text file content
        
        Args:
            file_path (str): Path to input text file
            target_language (str): Target language code or name
            output_path (str): Path to output translated file
            source_language (str): Source language code (auto-detect if "auto")
            
        Returns:
            Dict: File translation result
        """
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return {
                    "success": False,
                    "message": "File is empty",
                    "input_file": file_path
                }
            
            # Translate content
            translation_result = self.translate(content, target_language, source_language)
            
            if not translation_result["success"]:
                return {
                    "success": False,
                    "message": f"Translation failed: {translation_result['message']}",
                    "input_file": file_path
                }
            
            # Write translated content to output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translation_result["translated_text"])
            
            return {
                "success": True,
                "input_file": file_path,
                "output_file": output_path,
                "source_language": translation_result["source_language"],
                "target_language": translation_result["target_language"],
                "original_length": len(content),
                "translated_length": len(translation_result["translated_text"]),
                "service_used": translation_result["service"]
            }
            
        except Exception as e:
            self.logger.error(f"Error translating file: {e}")
            return {
                "success": False,
                "message": f"File translation error: {str(e)}",
                "input_file": file_path
            }