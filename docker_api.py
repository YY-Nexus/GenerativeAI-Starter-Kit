from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import json

app = FastAPI(
    title="GenerativeAI-Starter-Kit API",
    description="A simple API for GenerativeAI-Starter-Kit demonstration",
    version="0.2.0",
)


class HealthResponse(BaseModel):
    status: str
    message: str
    version: str


class TextRequest(BaseModel):
    text: str
    max_length: int = 100


class TextResponse(BaseModel):
    result: str
    processed: bool


@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {
        "message": "GenerativeAI-Starter-Kit API is running!",
        "status": "healthy",
        "version": "0.2.0",
        "endpoints": ["/", "/health", "/docs", "/process-text", "/demo"],
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    return HealthResponse(
        status="healthy", message="Service is running normally", version="0.2.0"
    )


@app.post("/process-text", response_model=TextResponse)
async def process_text(request: TextRequest):
    """处理文本的简单示例"""
    try:
        # 简单的文本处理演示
        processed_text = f"Processed: {request.text[:request.max_length]}"
        if len(request.text) > request.max_length:
            processed_text += "..."

        return TextResponse(result=processed_text, processed=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/demo")
async def demo_endpoint():
    """演示端点"""
    return {
        "demo": "This is a demo endpoint",
        "features": [
            "FastAPI framework",
            "Docker containerization",
            "Health checks",
            "API documentation",
            "Error handling",
        ],
        "usage": {
            "health_check": "GET /health",
            "process_text": "POST /process-text",
            "documentation": "GET /docs",
        },
    }


@app.get("/info")
async def get_info():
    """获取系统信息"""
    return {
        "app_name": "GenerativeAI-Starter-Kit",
        "python_version": "3.11",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "container": True,
        "timestamp": "2025-09-25",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
