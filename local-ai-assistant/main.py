#!/usr/bin/env python3
"""
Multi-Task AI Assistant
Main entry point for the application
"""

import sys
import os
import argparse
from config import Config
from scripts.wikipedia_query import WikipediaQuery
from scripts.document_reader import DocumentReader
from scripts.image_analysis import ImageAnalysis
from scripts.video_analysis import VideoAnalysis
from scripts.translator import Translator

class MultiTaskAIAssistant:
    def __init__(self):
        self.config = Config()
        self.wikipedia = WikipediaQuery()
        self.document_reader = DocumentReader()
        self.image_analysis = ImageAnalysis()
        self.video_analysis = VideoAnalysis()
        self.translator = Translator()
    
    def display_menu(self):
        """Display main menu options"""
        print("\n" + "="*50)
        print("Multi-Task AI Assistant")
        print("="*50)
        print("1. Wikipedia Query")
        print("2. Document Reader")
        print("3. Image Analysis")
        print("4. Video Analysis")
        print("5. Text Translation")
        print("6. Exit")
        print("="*50)
    
    def run_interactive_mode(self):
        """Run the assistant in interactive mode"""
        while True:
            self.display_menu()
            choice = input("Select an option (1-6): ").strip()
            
            if choice == "1":
                query = input("Enter your Wikipedia query: ")
                result = self.wikipedia.search(query)
                print(f"\nResult: {result}")
            
            elif choice == "2":
                file_path = input("Enter document file path: ")
                result = self.document_reader.read_document(file_path)
                print(f"\nDocument content: {result}")
            
            elif choice == "3":
                image_path = input("Enter image file path: ")
                result = self.image_analysis.analyze_image(image_path)
                print(f"\nImage analysis: {result}")
            
            elif choice == "4":
                video_path = input("Enter video file path: ")
                result = self.video_analysis.analyze_video(video_path)
                print(f"\nVideo analysis: {result}")
            
            elif choice == "5":
                text = input("Enter text to translate: ")
                target_lang = input("Enter target language (e.g., 'en', 'tr', 'de'): ")
                result = self.translator.translate(text, target_lang)
                print(f"\nTranslation: {result}")
            
            elif choice == "6":
                print("Goodbye!")
                break
            
            else:
                print("Invalid option. Please try again.")
    
    def run_command_mode(self, args):
        """Run the assistant in command mode"""
        if args.wikipedia:
            result = self.wikipedia.search(args.wikipedia)
            print(result)
        
        elif args.document:
            result = self.document_reader.read_document(args.document)
            print(result)
        
        elif args.image:
            result = self.image_analysis.analyze_image(args.image)
            print(result)
        
        elif args.video:
            result = self.video_analysis.analyze_video(args.video)
            print(result)
        
        elif args.translate:
            result = self.translator.translate(args.translate, args.target_lang or 'en')
            print(result)

def main():
    parser = argparse.ArgumentParser(description='Multi-Task AI Assistant')
    parser.add_argument('--wikipedia', help='Search Wikipedia')
    parser.add_argument('--document', help='Read document file')
    parser.add_argument('--image', help='Analyze image file')
    parser.add_argument('--video', help='Analyze video file')
    parser.add_argument('--translate', help='Translate text')
    parser.add_argument('--target-lang', help='Target language for translation')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    assistant = MultiTaskAIAssistant()
    
    # If no arguments provided or interactive flag is set, run interactive mode
    if len(sys.argv) == 1 or args.interactive:
        assistant.run_interactive_mode()
    else:
        assistant.run_command_mode(args)

if __name__ == "__main__":
    main()