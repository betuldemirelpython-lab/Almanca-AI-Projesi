"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
FastAPI Backend Application (api.py)
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from models import (
    TopicSummaryRequest, TopicSummaryResponse,
    WritingAnalysisRequest, WritingAnalysisResponse,
    StoryRequest, StoryResponse,
    VerbConjugationRequest, VerbConjugationResponse,
    TranslationRequest, TranslationResponse,
    PDFExportRequest, GermanLevelEnum, AIProviderEnum, TranslationDirectionEnum
)
from database import init_db, get_db, SavedAnalysis, SavedConjugation, FavoriteWord
from prompts import GERMAN_LEVELS_CATALOG
from ai_service import AIService
from contract_service import ContractService

# App Initialization
app = FastAPI(
    title="Yapay Zeka Destekli Almanca Öğrenme Projesi API",
    description="Google Gemini 2.5 Flash / Groq LLaMA 3.3 Destekli Almanca Öğrenme Servisi - Dev: Betül Altınkaynak Demirel",
    version="2.2.0"
)

# CORS Policy - Enable Vercel & Localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
ai_service = AIService()
contract_service = ContractService()


@app.on_event("startup")
def on_startup():
    init_db()
    print("🚀 FastAPI Server Started Successfully with AI Writing Coach & Evaluator!")


@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "project": "Yapay Zeka Destekli Almanca Öğrenme Projesi",
        "developer": "Betül Altınkaynak Demirel",
        "ai_models": ["Google Gemini 2.5 Flash", "Groq LLaMA 3.3"],
        "modules": ["A1-C2 Curriculum", "AI Writing Evaluator & Coach", "Audio Interactive Stories", "Verb Conjugation Matrix", "Dictionary", "PDF Export"],
        "version": "2.2.0"
    }


@app.get("/api/levels")
def get_levels_catalog():
    return {
        "status": "success",
        "catalog": GERMAN_LEVELS_CATALOG
    }


@app.post("/api/analyze-topic", response_model=TopicSummaryResponse)
async def analyze_topic(request: TopicSummaryRequest, db: Session = Depends(get_db)):
    try:
        result = await ai_service.analyze_topic(
            topic=request.topic,
            level=request.level.value if request.level else "A1",
            provider=request.provider.value if request.provider else "gemini"
        )
        
        saved_entry = SavedAnalysis(
            title=f"{request.level.value if request.level else 'A1'} - {request.topic}",
            level=request.level.value if request.level else "A1",
            topic=request.topic,
            provider=request.provider.value if request.provider else "gemini",
            summary_data=result
        )
        db.add(saved_entry)
        db.commit()

        return TopicSummaryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Konu analizi hatası: {str(e)}")


@app.post("/api/evaluate-writing", response_model=WritingAnalysisResponse)
async def evaluate_writing(request: WritingAnalysisRequest):
    """Kullanıcının yazdığı Almanca metni analiz eder, 100 üzerinden skorlar ve hatalarını düzeltir."""
    try:
        result = await ai_service.evaluate_writing(
            text=request.text,
            target_level=request.target_level.value if request.target_level else "B1",
            provider=request.provider.value if request.provider else "gemini"
        )
        return WritingAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metin değerlendirme hatası: {str(e)}")


@app.post("/api/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        result = await ai_service.generate_story(
            level=request.level.value if request.level else "A1",
            theme=request.topic_theme or "Günlük Yaşam",
            provider=request.provider.value if request.provider else "gemini"
        )
        return StoryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hikaye üretme hatası: {str(e)}")


@app.post("/api/conjugate", response_model=VerbConjugationResponse)
async def conjugate_verb(request: VerbConjugationRequest, db: Session = Depends(get_db)):
    try:
        result = await ai_service.conjugate_verb(
            verb=request.verb,
            provider=request.provider.value if request.provider else "gemini"
        )

        existing = db.query(SavedConjugation).filter(SavedConjugation.verb == request.verb.strip().lower()).first()
        if not existing:
            saved_verb = SavedConjugation(
                verb=request.verb.strip().lower(),
                turkish_meaning=result.get("turkish_meaning", ""),
                is_regular=result.get("is_regular", True),
                auxiliary_verb=result.get("auxiliary_verb", "haben"),
                conjugation_data=result
            )
            db.add(saved_verb)
            db.commit()

        return VerbConjugationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fiil çekimi hatası: {str(e)}")


@app.post("/api/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        result = await ai_service.translate_text(
            text=request.text,
            direction=request.direction.value if request.direction else "de-tr",
            provider=request.provider.value if request.provider else "gemini"
        )
        return TranslationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çeviri hatası: {str(e)}")


@app.post("/api/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    level: str = Form("A1"),
    provider: str = Form("gemini")
):
    try:
        contents = await file.read()
        extracted_text = contract_service.extract_text_from_file(contents, file.filename)
        
        analysis_result = await ai_service.analyze_topic(
            topic=f"Belge Analizi: {file.filename}",
            level=level,
            provider=provider
        )

        return {
            "filename": file.filename,
            "extracted_character_count": len(extracted_text),
            "text_preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "analysis": analysis_result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Belge işleme hatası: {str(e)}")


@app.post("/api/export-pdf")
async def export_pdf(request: PDFExportRequest):
    try:
        pdf_bytes = contract_service.generate_pdf_report(
            title=request.title,
            content_markdown=request.content_markdown,
            author=request.author or "Betül Altınkaynak Demirel",
            subtitle=request.subtitle or "Yapay Zeka Destekli Almanca Öğrenme Raporu"
        )
        
        headers = {
            "Content-Disposition": f"attachment; filename=Almanca_Rapor_{request.title.replace(' ', '_')}.pdf"
        }
        return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF oluşturma hatası: {str(e)}")


@app.get("/api/history")
def get_history(db: Session = Depends(get_db)):
    analyses = db.query(SavedAnalysis).order_by(SavedAnalysis.created_at.desc()).limit(20).all()
    conjugations = db.query(SavedConjugation).order_by(SavedConjugation.created_at.desc()).limit(20).all()

    return {
        "saved_analyses": [
            {
                "id": a.id,
                "title": a.title,
                "level": a.level,
                "topic": a.topic,
                "created_at": a.created_at.isoformat()
            } for a in analyses
        ],
        "saved_verbs": [
            {
                "id": v.id,
                "verb": v.verb,
                "meaning": v.turkish_meaning,
                "auxiliary": v.auxiliary_verb,
                "created_at": v.created_at.isoformat()
            } for v in conjugations
        ]
    }


if os.path.exists("index.html"):
    @app.get("/")
    def serve_frontend():
        return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
