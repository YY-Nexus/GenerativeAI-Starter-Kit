"""
FastAPI Server for GenerativeAI Starter Kit
==========================================

This module provides a REST API server that exposes the core functionality
of the GenerativeAI Starter Kit including RAG, multimodal, and fine-tuning capabilities.

Author: GenerativeAI-Starter-Kit
License: MIT
"""

import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import yaml

# Add parent directory to path to import examples
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.rag.simple_rag import SimpleRAG, RAGConfig
from examples.multimodal.image_text_app import MultimodalApp
from PIL import Image
import io


# Pydantic models for API
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    response: str


class DocumentRequest(BaseModel):
    documents: List[str]
    metadata: Optional[List[Dict[str, Any]]] = None


class ImageAnalysisRequest(BaseModel):
    query: Optional[str] = None


class ImageAnalysisResponse(BaseModel):
    caption: str
    query: Optional[str] = None
    similarity: Optional[float] = None
    size: List[int]
    mode: str


# Initialize FastAPI app
app = FastAPI(
    title="GenerativeAI Starter Kit API",
    description="REST API for RAG, multimodal, and fine-tuning capabilities",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
rag_system: Optional[SimpleRAG] = None
multimodal_app: Optional[MultimodalApp] = None


def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file"""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "configs", "config.yaml"
    )

    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        # Return default config
        return {
            "models": {
                "embedding": {
                    "name": "sentence-transformers/all-MiniLM-L6-v2",
                    "device": "cpu",
                }
            },
            "vector_db": {
                "type": "chroma",
                "collection_name": "api_documents",
                "persist_directory": "./api_chroma_db",
            },
            "rag": {"chunk_size": 1000, "chunk_overlap": 200, "top_k": 5},
        }


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global rag_system, multimodal_app

    print("🚀 Starting GenerativeAI Starter Kit API...")

    # Load configuration
    config_dict = load_config()

    # Initialize RAG system
    try:
        print("📊 Initializing RAG system...")
        rag_config = RAGConfig(
            embedding_model=config_dict["models"]["embedding"]["name"],
            chunk_size=config_dict["rag"]["chunk_size"],
            chunk_overlap=config_dict["rag"]["chunk_overlap"],
            top_k=config_dict["rag"]["top_k"],
            collection_name=config_dict["vector_db"]["collection_name"],
            persist_directory=config_dict["vector_db"]["persist_directory"],
        )
        rag_system = SimpleRAG(rag_config)
        rag_system.initialize()
        print("✅ RAG system initialized")
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")

    # Initialize multimodal app
    try:
        print("🎨 Initializing multimodal app...")
        multimodal_app = MultimodalApp()
        multimodal_app.initialize()
        print("✅ Multimodal app initialized")
    except Exception as e:
        print(f"❌ Failed to initialize multimodal app: {e}")

    print("✅ API server startup complete!")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "GenerativeAI Starter Kit API",
        "version": "1.0.0",
        "endpoints": {
            "rag": {"add_documents": "/rag/documents", "query": "/rag/query"},
            "multimodal": {"analyze_image": "/multimodal/analyze"},
            "health": "/health",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_available": rag_system is not None,
        "multimodal_available": multimodal_app is not None,
    }


# RAG Endpoints
@app.post("/rag/documents")
async def add_documents(request: DocumentRequest):
    """Add documents to the RAG system"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not available")

    try:
        rag_system.add_documents(request.documents, request.metadata)
        return {
            "message": f"Successfully added {len(request.documents)} documents",
            "document_count": len(request.documents),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add documents: {str(e)}"
        )


@app.post("/rag/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Query the RAG system"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not available")

    try:
        # Search for relevant documents
        results = rag_system.search(request.query, request.top_k)

        # Generate response
        context_docs = [result["document"] for result in results]
        response = rag_system.generate_response(request.query, context_docs)

        return QueryResponse(query=request.query, results=results, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


# Multimodal Endpoints
@app.post("/multimodal/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...), query: Optional[str] = None):
    """Analyze an uploaded image"""
    if not multimodal_app:
        raise HTTPException(status_code=503, detail="Multimodal app not available")

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read and process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Analyze image
        results = multimodal_app.analyze_image(image, query)

        return ImageAnalysisResponse(
            caption=results["caption"],
            query=query,
            similarity=results.get("query_similarity"),
            size=list(results["size"]),
            mode=results["mode"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")


# Additional utility endpoints
@app.get("/rag/stats")
async def get_rag_stats():
    """Get RAG system statistics"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not available")

    try:
        # Get collection info
        collection_count = rag_system.collection.count() if rag_system.collection else 0

        return {
            "collection_name": rag_system.config.collection_name,
            "document_count": collection_count,
            "embedding_model": rag_system.config.embedding_model,
            "chunk_size": rag_system.config.chunk_size,
            "top_k": rag_system.config.top_k,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Start the GenerativeAI Starter Kit API server"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

    print(f"🌐 Starting API server on http://{args.host}:{args.port}")
    print("📖 API documentation available at http://{args.host}:{args.port}/docs")

    uvicorn.run("api_server:app", host=args.host, port=args.port, reload=args.reload)
