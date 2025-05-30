"""
Video Analysis Module
Handles video processing and analysis
"""

import os
import logging
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
import sys

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
            
            # Open video
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
                "frame_analysis": self._analyze_frames(cap),
                "motion_analysis": self._analyze_motion(cap),
                "scene_detection": self._detect_scenes(cap),
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
    
    def _get_basic_info(self, video_path: str, cap: cv2.VideoCapture) -> Dict:
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
    
    def _analyze_frames(self, cap: cv2.VideoCapture) -> Dict:
        """Analyze video frames"""
        try:
            # Reset to beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Sample frames at regular intervals
            sample_interval = max(1, frame_count // 10)  # Sample 10 frames max
            
            brightness_values = []
            contrast_values = []
            sampled_frames = 0
            
            for i in range(0, frame_count, sample_interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Convert to grayscale for analysis
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Calculate brightness and contrast
                brightness = np.mean(gray)
                contrast = np.std(gray)
                
                brightness_values.append(brightness)
                contrast_values.append(contrast)
                sampled_frames += 1
            
            return {
                "sampled_frames": sampled_frames,
                "average_brightness": round(np.mean(brightness_values), 2) if brightness_values else 0,
                "brightness_std": round(np.std(brightness_values), 2) if brightness_values else 0,
                "average_contrast": round(np.mean(contrast_values), 2) if contrast_values else 0,
                "contrast_std": round(np.std(contrast_values), 2) if contrast_values else 0,
                "brightness_range": {
                    "min": round(min(brightness_values), 2) if brightness_values else 0,
                    "max": round(max(brightness_values), 2) if brightness_values else 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing frames: {e}")
            return {}
    
    def _analyze_motion(self, cap: cv2.VideoCapture) -> Dict:
        """Analyze motion in video using optical flow"""
        try:
            # Reset to beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            ret, frame1 = cap.read()
            if not ret:
                return {}
            
            # Convert to grayscale
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            
            motion_scores = []
            frame_count = 0
            max_frames_to_analyze = 50  # Limit analysis for performance
            
            while frame_count < max_frames_to_analyze:
                ret, frame2 = cap.read()
                if not ret:
                    break
                
                gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                
                # Calculate optical flow
                flow = cv2.calcOpticalFlowPyrLK(
                    gray1, gray2,
                    np.array([[x, y] for x in range(0, gray1.shape[1], 20) 
                             for y in range(0, gray1.shape[0], 20)], dtype=np.float32).reshape(-1, 1, 2),
                    None
                )
                
                if flow[0] is not None:
                    # Calculate motion magnitude
                    motion_vectors = flow[0] - np.array([[x, y] for x in range(0, gray1.shape[1], 20) 
                                                        for y in range(0, gray1.shape[0], 20)], dtype=np.float32).reshape(-1, 1, 2)
                    motion_magnitude = np.sqrt(motion_vectors[:, 0, 0]**2 + motion_vectors[:, 0, 1]**2)
                    avg_motion = np.mean(motion_magnitude)
                    motion_scores.append(avg_motion)
                
                gray1 = gray2
                frame_count += 1
            
            if motion_scores:
                avg_motion = np.mean(motion_scores)
                motion_category = "High" if avg_motion > 5 else "Medium" if avg_motion > 2 else "Low"
            else:
                avg_motion = 0
                motion_category = "Unknown"
            
            return {
                "frames_analyzed": frame_count,
                "average_motion": round(avg_motion, 2),
                "motion_category": motion_category,
                "motion_std": round(np.std(motion_scores), 2) if motion_scores else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing motion: {e}")
            return {}
    
    def _detect_scenes(self, cap: cv2.VideoCapture) -> Dict:
        """Basic scene detection using frame difference"""
        try:
            # Reset to beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            ret, prev_frame = cap.read()
            if not ret:
                return {}
            
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            
            scene_changes = []
            frame_number = 0
            threshold = 30  # Threshold for scene change detection
            
            while True:
                ret, curr_frame = cap.read()
                if not ret:
                    break
                
                curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
                
                # Calculate frame difference
                diff = cv2.absdiff(prev_gray, curr_gray)
                mean_diff = np.mean(diff)
                
                # If difference is above threshold, it's likely a scene change
                if mean_diff > threshold:
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    timestamp = frame_number / fps if fps > 0 else 0
                    scene_changes.append({
                        "frame": frame_number,
                        "timestamp": round(timestamp, 2),
                        "difference_score": round(mean_diff, 2)
                    })
                
                prev_gray = curr_gray
                frame_number += 1
                
                # Limit analysis for performance
                if frame_number > 1000:
                    break
            
            return {
                "scene_changes_detected": len(scene_changes),
                "scene_changes": scene_changes[:10],  # Return first 10 changes
                "frames_analyzed": frame_number
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting scenes: {e}")
            return {}
    
    def _analyze_audio(self, video_path: str) -> Dict:
        """Analyze audio track of the video"""
        try:
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
    
    def extract_frames(self, video_path: str, output_dir: str, interval_seconds: int = 30) -> Dict:
        """Extract frames from video at specified intervals"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * interval_seconds)
            
            frame_count = 0
            extracted_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps
                    output_path = os.path.join(output_dir, f"frame_{timestamp:.1f}s.jpg")
                    cv2.imwrite(output_path, frame)
                    extracted_count += 1
                
                frame_count += 1
            
            cap.release()
            
            return {
                "success": True,
                "total_frames": frame_count,
                "extracted_frames": extracted_count,
                "output_directory": output_dir,
                "interval_seconds": interval_seconds
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting frames: {e}")
            return {"success": False, "message": str(e)}
    
    def create_thumbnail(self, video_path: str, output_path: str, timestamp: float = 1.0) -> Dict:
        """Create a thumbnail from video at specified timestamp"""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(fps * timestamp)
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            if ret:
                cv2.imwrite(output_path, frame)
                cap.release()
                return {
                    "success": True,
                    "thumbnail_path": output_path,
                    "timestamp": timestamp
                }
            else:
                cap.release()
                return {"success": False, "message": "Could not extract frame"}
                
        except Exception as e:
            self.logger.error(f"Error creating thumbnail: {e}")
            return {"success": False, "message": str(e)}