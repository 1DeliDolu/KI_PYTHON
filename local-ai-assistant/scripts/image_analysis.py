"""
Image Analysis Module
Handles image processing and analysis using computer vision
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import sys

# Add parent directory to path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class ImageAnalysis:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
    
    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze image and extract various features
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict: Analysis results including objects, colors, etc.
        """
        try:
            # Validate file
            is_valid, message = self.config.validate_file(image_path, "image")
            if not is_valid:
                return {
                    "success": False,
                    "message": message,
                    "analysis": {}
                }
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return {
                    "success": False,
                    "message": "Could not load image",
                    "analysis": {}
                }
            
            # Perform various analyses
            analysis_results = {
                "basic_info": self._get_basic_info(image_path, image),
                "color_analysis": self._analyze_colors(image),
                "edge_detection": self._detect_edges(image),
                "face_detection": self._detect_faces(image),
                "object_detection": self._detect_objects(image),
                "image_quality": self._assess_quality(image)
            }
            
            return {
                "success": True,
                "file_path": image_path,
                "analysis": analysis_results
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing image '{image_path}': {e}")
            return {
                "success": False,
                "message": f"Error analyzing image: {str(e)}",
                "analysis": {}
            }
    
    def _get_basic_info(self, image_path: str, image: np.ndarray) -> Dict:
        """Get basic image information"""
        try:
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            
            # Get file size
            file_size = os.path.getsize(image_path)
            
            return {
                "dimensions": f"{width}x{height}",
                "width": width,
                "height": height,
                "channels": channels,
                "color_space": "BGR" if channels == 3 else "Grayscale",
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "aspect_ratio": round(width / height, 2),
                "total_pixels": width * height
            }
            
        except Exception as e:
            self.logger.error(f"Error getting basic info: {e}")
            return {}
    
    def _analyze_colors(self, image: np.ndarray) -> Dict:
        """Analyze color distribution in the image"""
        try:
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Calculate color statistics
            mean_color = np.mean(image_rgb, axis=(0, 1))
            
            # Get dominant colors using K-means clustering
            dominant_colors = self._get_dominant_colors(image_rgb, k=5)
            
            # Calculate brightness
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            
            # Calculate contrast
            contrast = np.std(gray)
            
            return {
                "mean_color_rgb": [int(c) for c in mean_color],
                "brightness": round(brightness, 2),
                "contrast": round(contrast, 2),
                "dominant_colors": dominant_colors,
                "color_temperature": self._estimate_color_temperature(mean_color)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing colors: {e}")
            return {}
    
    def _get_dominant_colors(self, image: np.ndarray, k: int = 5) -> List[List[int]]:
        """Get dominant colors using K-means clustering"""
        try:
            # Reshape image to be a list of pixels
            pixels = image.reshape(-1, 3)
            
            # Use K-means clustering
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get the colors
            colors = kmeans.cluster_centers_
            
            # Convert to integers and return
            return [[int(c) for c in color] for color in colors]
            
        except ImportError:
            # Fallback if sklearn is not available
            return []
        except Exception as e:
            self.logger.error(f"Error getting dominant colors: {e}")
            return []
    
    def _estimate_color_temperature(self, mean_color: np.ndarray) -> str:
        """Estimate color temperature based on mean color"""
        try:
            r, g, b = mean_color
            
            # Simple heuristic for color temperature
            if b > r and b > g:
                return "Cool (Blue-ish)"
            elif r > b and r > g:
                return "Warm (Red-ish)"
            else:
                return "Neutral"
                
        except Exception:
            return "Unknown"
    
    def _detect_edges(self, image: np.ndarray) -> Dict:
        """Detect edges in the image using Canny edge detection"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Count edge pixels
            edge_pixel_count = np.sum(edges > 0)
            total_pixels = gray.shape[0] * gray.shape[1]
            edge_density = edge_pixel_count / total_pixels
            
            return {
                "edge_pixel_count": int(edge_pixel_count),
                "total_pixels": int(total_pixels),
                "edge_density": round(edge_density, 4),
                "edge_density_percentage": round(edge_density * 100, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting edges: {e}")
            return {}
    
    def _detect_faces(self, image: np.ndarray) -> Dict:
        """Detect faces in the image using Haar cascades"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            face_info = []
            for (x, y, w, h) in faces:
                face_info.append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area": int(w * h)
                })
            
            return {
                "face_count": len(faces),
                "faces": face_info
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting faces: {e}")
            return {"face_count": 0, "faces": []}
    
    def _detect_objects(self, image: np.ndarray) -> Dict:
        """Basic object detection using contours"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by area
            min_area = 1000
            objects = []
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    objects.append({
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": int(area)
                    })
            
            return {
                "object_count": len(objects),
                "objects": objects,
                "total_contours": len(contours)
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting objects: {e}")
            return {"object_count": 0, "objects": []}
    
    def _assess_quality(self, image: np.ndarray) -> Dict:
        """Assess image quality"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate Laplacian variance (blur detection)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate noise level (using standard deviation)
            noise_level = np.std(gray)
            
            # Determine quality score (simple heuristic)
            if laplacian_var > 100:
                sharpness = "Sharp"
            elif laplacian_var > 50:
                sharpness = "Moderate"
            else:
                sharpness = "Blurry"
            
            return {
                "laplacian_variance": round(laplacian_var, 2),
                "sharpness": sharpness,
                "noise_level": round(noise_level, 2),
                "estimated_quality": "Good" if laplacian_var > 100 and noise_level < 50 else "Fair" if laplacian_var > 50 else "Poor"
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing quality: {e}")
            return {}
    
    def resize_image(self, image_path: str, output_path: str, width: int, height: int) -> Dict:
        """Resize image to specified dimensions"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {"success": False, "message": "Could not load image"}
            
            resized = cv2.resize(image, (width, height))
            cv2.imwrite(output_path, resized)
            
            return {
                "success": True,
                "original_size": f"{image.shape[1]}x{image.shape[0]}",
                "new_size": f"{width}x{height}",
                "output_path": output_path
            }
            
        except Exception as e:
            self.logger.error(f"Error resizing image: {e}")
            return {"success": False, "message": str(e)}
    
    def convert_format(self, input_path: str, output_path: str) -> Dict:
        """Convert image to different format"""
        try:
            image = Image.open(input_path)
            image.save(output_path)
            
            return {
                "success": True,
                "input_format": os.path.splitext(input_path)[1],
                "output_format": os.path.splitext(output_path)[1],
                "output_path": output_path
            }
            
        except Exception as e:
            self.logger.error(f"Error converting image format: {e}")
            return {"success": False, "message": str(e)}