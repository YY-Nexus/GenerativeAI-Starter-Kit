"""
Multimodal Image-Text Application
=================================

This example demonstrates a multimodal AI application that can:
- Analyze and describe images
- Generate images from text descriptions
- Search images using text queries
- Answer questions about images

Author: GenerativeAI-Starter-Kit
License: MIT
"""

import os
import torch
import numpy as np
from PIL import Image
from typing import List, Dict, Any, Optional
import requests
from io import BytesIO

# CLIP for image-text understanding
try:
    import clip

    CLIP_AVAILABLE = True
except ImportError:
    print(
        "⚠️ CLIP not available. Install with: pip install git+https://github.com/openai/CLIP.git"
    )
    CLIP_AVAILABLE = False

# Transformers for image captioning
from transformers import BlipProcessor, BlipForConditionalGeneration

# Gradio for web interface
import gradio as gr


class MultimodalApp:
    """A multimodal application for image-text tasks"""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model = None
        self.clip_preprocess = None
        self.caption_processor = None
        self.caption_model = None

        print(f"🖥️  Using device: {self.device}")

    def initialize(self):
        """Initialize models"""
        print("🚀 Initializing multimodal models...")

        # Initialize CLIP for image-text similarity
        if CLIP_AVAILABLE:
            try:
                print("📊 Loading CLIP model...")
                self.clip_model, self.clip_preprocess = clip.load(
                    "ViT-B/32", device=self.device
                )
                print("✅ CLIP model loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load CLIP: {e}")

        # Initialize BLIP for image captioning
        try:
            print("🖼️  Loading BLIP model for image captioning...")
            self.caption_processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            self.caption_model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            self.caption_model.to(self.device)
            print("✅ BLIP model loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load BLIP: {e}")

    def load_image(self, image_path: str) -> Image.Image:
        """Load image from file path or URL"""
        try:
            if image_path.startswith(("http://", "https://")):
                response = requests.get(image_path)
                image = Image.open(BytesIO(response.content)).convert("RGB")
            else:
                image = Image.open(image_path).convert("RGB")
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image: {e}")

    def generate_caption(self, image: Image.Image) -> str:
        """Generate a caption for the image"""
        if not self.caption_model or not self.caption_processor:
            return "Caption model not available"

        try:
            # Process image
            inputs = self.caption_processor(image, return_tensors="pt").to(self.device)

            # Generate caption
            with torch.no_grad():
                out = self.caption_model.generate(**inputs, max_length=50, num_beams=3)

            caption = self.caption_processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            return f"Error generating caption: {e}"

    def calculate_similarity(self, image: Image.Image, text: str) -> float:
        """Calculate similarity between image and text using CLIP"""
        if not CLIP_AVAILABLE or not self.clip_model:
            return 0.0

        try:
            # Preprocess image and text
            image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)
            text_input = clip.tokenize([text]).to(self.device)

            # Calculate features
            with torch.no_grad():
                image_features = self.clip_model.encode_image(image_input)
                text_features = self.clip_model.encode_text(text_input)

                # Calculate cosine similarity
                similarity = torch.cosine_similarity(
                    image_features, text_features
                ).item()

            return similarity
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0

    def search_images(self, query: str, image_paths: List[str]) -> List[Dict[str, Any]]:
        """Search images based on text query"""
        results = []

        for image_path in image_paths:
            try:
                image = self.load_image(image_path)
                similarity = self.calculate_similarity(image, query)

                results.append(
                    {"path": image_path, "similarity": similarity, "image": image}
                )
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

    def analyze_image(
        self, image: Image.Image, query: Optional[str] = None
    ) -> Dict[str, Any]:
        """Comprehensive image analysis"""
        results = {
            "caption": self.generate_caption(image),
            "size": image.size,
            "mode": image.mode,
        }

        if query and CLIP_AVAILABLE:
            results["query_similarity"] = self.calculate_similarity(image, query)
            results["query"] = query

        return results


def create_gradio_interface():
    """Create a Gradio web interface for the multimodal app"""

    # Initialize the app
    app = MultimodalApp()
    app.initialize()

    def process_image(image, query):
        """Process image for Gradio interface"""
        if image is None:
            return "Please upload an image"

        try:
            # Convert to PIL Image if needed
            if not isinstance(image, Image.Image):
                image = Image.fromarray(image)

            # Analyze image
            results = app.analyze_image(image, query)

            output = f"📷 **Image Analysis**\n\n"
            output += f"**Caption:** {results['caption']}\n\n"
            output += (
                f"**Size:** {results['size'][0]} x {results['size'][1]} pixels\n\n"
            )

            if query and "query_similarity" in results:
                similarity_percentage = results["query_similarity"] * 100
                output += f"**Query Similarity:** {similarity_percentage:.1f}%\n"
                output += f"**Query:** {results['query']}\n\n"

            return output

        except Exception as e:
            return f"Error processing image: {e}"

    # Create Gradio interface
    interface = gr.Interface(
        fn=process_image,
        inputs=[
            gr.Image(type="pil", label="Upload Image"),
            gr.Textbox(
                label="Optional: Text Query",
                placeholder="Describe what you're looking for...",
            ),
        ],
        outputs=gr.Markdown(label="Analysis Results"),
        title="🎨 Multimodal Image-Text Application",
        description="""
        This application demonstrates multimodal AI capabilities:

        1. **Image Captioning**: Automatically generates descriptions for uploaded images
        2. **Image-Text Similarity**: Measures how well your text query matches the image
        3. **Comprehensive Analysis**: Provides technical details about the image

        **Instructions:**
        - Upload an image using the interface
        - Optionally, enter a text query to see similarity scores
        - View the generated caption and analysis results
        """,
        examples=[
            [None, "a cat sitting on a table"],
            [None, "a beautiful sunset over mountains"],
            [None, "people walking in a city street"],
        ],
    )

    return interface


def demo_multimodal():
    """Demonstrate multimodal capabilities with sample images"""
    print("🎯 Multimodal Application Demo")
    print("=" * 50)

    app = MultimodalApp()
    app.initialize()

    # Create a sample image (colored rectangle)
    sample_image = Image.new("RGB", (200, 100), color="blue")

    print("\n🖼️  Analyzing sample image...")
    results = app.analyze_image(sample_image, "a blue rectangle")

    print(f"Caption: {results['caption']}")
    print(f"Size: {results['size']}")

    if "query_similarity" in results:
        print(f"Query similarity: {results['query_similarity']:.3f}")

    print("\n🌐 To use the web interface, run:")
    print("python examples/multimodal/image_text_app.py --web")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        print("🌐 Starting web interface...")
        interface = create_gradio_interface()
        interface.launch(share=True)
    else:
        demo_multimodal()
