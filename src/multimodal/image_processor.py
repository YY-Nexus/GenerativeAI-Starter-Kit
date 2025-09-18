"""
Image processing capabilities for multimodal AI applications
"""
import os
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import base64
import io

try:
    from PIL import Image
    import cv2
    import numpy as np
except ImportError:
    print("Warning: PIL, OpenCV, or NumPy not installed. Some image features may not work.")
    print("Install with: pip install pillow opencv-python numpy")


class ImageProcessor:
    """Image processing and analysis for multimodal applications"""
    
    def __init__(self, max_size: tuple = (1024, 1024)):
        """
        Initialize image processor
        
        Args:
            max_size: Maximum image dimensions (width, height)
        """
        self.max_size = max_size
    
    def load_image(self, image_path: Union[str, Path]) -> Image.Image:
        """
        Load image from file path
        
        Args:
            image_path: Path to image file
            
        Returns:
            PIL Image object
        """
        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            raise ValueError(f"Error loading image from {image_path}: {str(e)}")
    
    def resize_image(self, image: Image.Image, 
                    max_size: Optional[tuple] = None) -> Image.Image:
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image: PIL Image object
            max_size: Maximum dimensions (width, height)
            
        Returns:
            Resized PIL Image object
        """
        max_size = max_size or self.max_size
        
        # Calculate new size maintaining aspect ratio
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    def image_to_base64(self, image: Image.Image, format: str = "JPEG") -> str:
        """
        Convert PIL Image to base64 string
        
        Args:
            image: PIL Image object
            format: Image format (JPEG, PNG, etc.)
            
        Returns:
            Base64 encoded string
        """
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def base64_to_image(self, base64_string: str) -> Image.Image:
        """
        Convert base64 string to PIL Image
        
        Args:
            base64_string: Base64 encoded image string
            
        Returns:
            PIL Image object
        """
        img_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(img_data))
        return image
    
    def extract_text_from_image(self, image: Union[str, Path, Image.Image]) -> str:
        """
        Extract text from image using OCR (requires pytesseract)
        
        Args:
            image: Image file path or PIL Image object
            
        Returns:
            Extracted text string
        """
        try:
            import pytesseract
        except ImportError:
            return "OCR not available. Install with: pip install pytesseract"
        
        if isinstance(image, (str, Path)):
            image = self.load_image(image)
        
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def detect_objects(self, image: Union[str, Path, Image.Image]) -> List[Dict[str, Any]]:
        """
        Detect objects in image (placeholder for actual object detection)
        In practice, you would use models like YOLO, COCO, etc.
        
        Args:
            image: Image file path or PIL Image object
            
        Returns:
            List of detected objects with bounding boxes and labels
        """
        if isinstance(image, (str, Path)):
            image = self.load_image(image)
        
        # Placeholder implementation
        # In practice, you would use pre-trained models like:
        # - YOLO (You Only Look Once)
        # - COCO dataset models
        # - Custom trained models
        
        return [
            {
                "label": "placeholder_object",
                "confidence": 0.5,
                "bbox": [0, 0, 100, 100],  # [x, y, width, height]
                "description": "Object detection requires additional models. See documentation for setup."
            }
        ]
    
    def analyze_image_properties(self, image: Union[str, Path, Image.Image]) -> Dict[str, Any]:
        """
        Analyze basic image properties
        
        Args:
            image: Image file path or PIL Image object
            
        Returns:
            Dictionary with image properties
        """
        if isinstance(image, (str, Path)):
            image_path = image
            image = self.load_image(image)
        else:
            image_path = "loaded_image"
        
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Calculate basic statistics
        properties = {
            "path": str(image_path),
            "format": image.format or "Unknown",
            "mode": image.mode,
            "size": image.size,  # (width, height)
            "dimensions": {
                "width": image.size[0],
                "height": image.size[1],
                "channels": len(img_array.shape) if len(img_array.shape) > 2 else 1
            },
            "color_stats": {
                "mean_brightness": float(np.mean(img_array)),
                "std_brightness": float(np.std(img_array)),
                "min_value": int(np.min(img_array)),
                "max_value": int(np.max(img_array))
            }
        }
        
        # Add color analysis for RGB images
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            properties["color_stats"]["mean_rgb"] = [
                float(np.mean(img_array[:, :, i])) for i in range(3)
            ]
        
        return properties
    
    def create_thumbnail(self, image: Union[str, Path, Image.Image], 
                        size: tuple = (128, 128)) -> Image.Image:
        """
        Create thumbnail of image
        
        Args:
            image: Image file path or PIL Image object
            size: Thumbnail size (width, height)
            
        Returns:
            Thumbnail PIL Image object
        """
        if isinstance(image, (str, Path)):
            image = self.load_image(image)
        
        # Create thumbnail
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        
        return thumbnail
    
    def apply_filters(self, image: Image.Image, 
                     filters: List[str]) -> Image.Image:
        """
        Apply basic filters to image
        
        Args:
            image: PIL Image object
            filters: List of filter names
            
        Returns:
            Filtered PIL Image object
        """
        try:
            from PIL import ImageFilter, ImageEnhance
        except ImportError:
            return image
        
        filtered_image = image.copy()
        
        for filter_name in filters:
            if filter_name == "blur":
                filtered_image = filtered_image.filter(ImageFilter.BLUR)
            elif filter_name == "sharpen":
                filtered_image = filtered_image.filter(ImageFilter.SHARPEN)
            elif filter_name == "edge":
                filtered_image = filtered_image.filter(ImageFilter.FIND_EDGES)
            elif filter_name == "enhance_contrast":
                enhancer = ImageEnhance.Contrast(filtered_image)
                filtered_image = enhancer.enhance(1.5)
            elif filter_name == "enhance_brightness":
                enhancer = ImageEnhance.Brightness(filtered_image)
                filtered_image = enhancer.enhance(1.2)
        
        return filtered_image
    
    def prepare_for_llm_vision(self, image: Union[str, Path, Image.Image],
                              max_size: tuple = (512, 512)) -> Dict[str, Any]:
        """
        Prepare image for LLM vision models (like GPT-4V)
        
        Args:
            image: Image file path or PIL Image object
            max_size: Maximum size for the image
            
        Returns:
            Dictionary with image data and metadata for LLM
        """
        if isinstance(image, (str, Path)):
            original_path = str(image)
            image = self.load_image(image)
        else:
            original_path = "loaded_image"
        
        # Resize image
        resized_image = self.resize_image(image, max_size)
        
        # Convert to base64
        base64_string = self.image_to_base64(resized_image)
        
        # Analyze properties
        properties = self.analyze_image_properties(resized_image)
        
        return {
            "base64": base64_string,
            "format": "JPEG",
            "properties": properties,
            "original_path": original_path,
            "prepared_for": "llm_vision",
            "data_url": f"data:image/jpeg;base64,{base64_string}"
        }


def create_sample_images(output_dir: Path):
    """Create sample images for testing"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Create a simple text image
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((50, 80), "Sample Text Image\nfor OCR Testing", 
                 fill='black', font=font)
        img.save(output_dir / "sample_text.png")
        
        # Create a gradient image
        gradient = Image.new('RGB', (300, 300), color='white')
        pixels = np.array(gradient)
        for i in range(300):
            for j in range(300):
                pixels[i, j] = [i//3, j//3, (i+j)//6]
        
        gradient = Image.fromarray(pixels.astype('uint8'))
        gradient.save(output_dir / "sample_gradient.png")
        
        print(f"Sample images created in {output_dir}")
        
    except Exception as e:
        print(f"Could not create sample images: {e}")


if __name__ == "__main__":
    # Example usage
    processor = ImageProcessor()
    
    # Create sample images for testing
    sample_dir = Path("./data/sample_datasets/images")
    create_sample_images(sample_dir)
    
    if (sample_dir / "sample_text.png").exists():
        # Test with sample image
        image_path = sample_dir / "sample_text.png"
        
        print(f"Processing image: {image_path}")
        
        # Load and analyze
        image = processor.load_image(image_path)
        properties = processor.analyze_image_properties(image)
        
        print("Image Properties:")
        for key, value in properties.items():
            print(f"  {key}: {value}")
        
        # Create thumbnail
        thumbnail = processor.create_thumbnail(image, (64, 64))
        thumbnail.save(sample_dir / "thumbnail.png")
        
        # Prepare for LLM
        llm_data = processor.prepare_for_llm_vision(image)
        print(f"\nPrepared for LLM: {len(llm_data['base64'])} characters in base64")
        
        # Extract text (if OCR is available)
        text = processor.extract_text_from_image(image)
        print(f"\nExtracted text: {text}")
    
    else:
        print("No sample images found. Run the script to generate them first.")