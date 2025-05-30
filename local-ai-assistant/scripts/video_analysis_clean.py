"""
Video Analysis Module
Handles video processing and analysis
"""

import os
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import sys

# Try to import MoviePy, fallback if not available
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("Warning: MoviePy not available. Video analysis features will be limited.")

# Try to import OpenCV, fallback if not available
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("Warning: OpenCV not available. Video analysis features will be limited.")

# Add parent directory to path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class VideoAnalysis:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
    
    def analyze_video(self, video_path: str) -> Dict:
        """
        Analyze video and extract various features
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            Dict: Analysis results including metadata, frames, motion, etc.
        """
        try:
            # Validate file
            is_valid, message = self.config.validate_file(video_path, "video")
            if not is_valid:
                return {
                    "success": False,
                    "message": message,
                    "analysis": {}
                }
            
            if not OPENCV_AVAILABLE and not MOVIEPY_AVAILABLE:
                return {
                    "success": False,
                    "message": "Neither OpenCV nor MoviePy available for video analysis",
                    "analysis": {}
                }
            
            if not OPENCV_AVAILABLE:
                # Use moviepy-only analysis
                return self._analyze_with_moviepy(video_path)
            
            # Open video with OpenCV
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {
                    "success": False,
                    "message": "Could not open video file",
                    "analysis": {}
                }
            
            # Perform various analyses
            analysis_results = {
                "basic_info": self._get_basic_info(video_path, cap),
                "audio_analysis": self._analyze_audio(video_path)
            }
            
            cap.release()
            
            return {
                "success": True,
                "file_path": video_path,
                "analysis": analysis_results
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing video '{video_path}': {e}")
            return {
                "success": False,
                "message": f"Error analyzing video: {str(e)}",
                "analysis": {}
            }
    
    def _analyze_with_moviepy(self, video_path: str) -> Dict:
        """MoviePy-only video analysis for when OpenCV is not available"""
        try:
            if not MOVIEPY_AVAILABLE:
                return {
                    "success": False,
                    "message": "MoviePy not available",
                    "analysis": {}
                }
            
            clip = VideoFileClip(video_path)
            
            analysis_results = {
                "basic_info": {
                    "duration_seconds": round(clip.duration, 2),
                    "duration_formatted": self._format_duration(clip.duration),
                    "fps": clip.fps,
                    "resolution": f"{clip.w}x{clip.h}" if hasattr(clip, 'w') and hasattr(clip, 'h') else "Unknown",
                    "width": clip.w if hasattr(clip, 'w') else 0,
                    "height": clip.h if hasattr(clip, 'h') else 0,
                    "file_size_bytes": os.path.getsize(video_path),
                    "file_size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 2)
                },
                "audio_analysis": self._analyze_audio(video_path),
                "opencv_status": "Not available - install OpenCV for full analysis"
            }
            
            clip.close()
            
            return {
                "success": True,
                "file_path": video_path,
                "analysis": analysis_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"MoviePy analysis failed: {str(e)}",
                "analysis": {}
            }
    
    def _get_basic_info(self, video_path: str, cap) -> Dict:
        """Get basic video information"""
        try:
            # Get video properties
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Calculate duration
            duration_seconds = frame_count / fps if fps > 0 else 0
            
            # Get file size
            file_size = os.path.getsize(video_path)
            
            return {
                "duration_seconds": round(duration_seconds, 2),
                "duration_formatted": self._format_duration(duration_seconds),
                "frame_count": frame_count,
                "fps": round(fps, 2),
                "resolution": f"{width}x{height}",
                "width": width,
                "height": height,
                "aspect_ratio": round(width / height, 2) if height > 0 else 0,
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "estimated_bitrate_kbps": round((file_size * 8) / (duration_seconds * 1000), 2) if duration_seconds > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting basic info: {e}")
            return {}
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in HH:MM:SS format"""
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        except:
            return "00:00:00"
    
    def _analyze_audio(self, video_path: str) -> Dict:
        """Analyze audio track of the video"""
        try:
            if not MOVIEPY_AVAILABLE:
                return {
                    "has_audio": False, 
                    "error": "MoviePy not available for audio analysis"
                }
            
            # Use moviepy to extract audio information
            clip = VideoFileClip(video_path)
            
            audio_info = {
                "has_audio": clip.audio is not None,
                "duration": round(clip.duration, 2) if clip.duration else 0
            }
            
            if clip.audio:
                audio_info.update({
                    "sample_rate": clip.audio.fps if hasattr(clip.audio, 'fps') else None,
                    "channels": getattr(clip.audio, 'nchannels', None)
                })
            
            clip.close()
            return audio_info
            
        except Exception as e:
            self.logger.error(f"Error analyzing audio: {e}")
            return {"has_audio": False, "error": str(e)}