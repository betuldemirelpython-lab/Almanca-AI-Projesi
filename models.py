"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
Pydantic v2 Veri Modelleri
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GermanLevelEnum(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class AIProviderEnum(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"


class TranslationDirectionEnum(str, Enum):
    DE_TO_TR = "de-tr"
    TR_TO_DE = "tr-de"


# --- Metin Analizi & Yazım Koçu Modelleri ---

class WritingAnalysisRequest(BaseModel):
    text: str = Field(..., description="Kullanıcının yazdığı Almanca metin")
    target_level: GermanLevelEnum = Field(GermanLevelEnum.B1, description="Hedeflenen Seviye (A1-C2)")
    provider: AIProviderEnum = Field(AIProviderEnum.GEMINI)


class ErrorItem(BaseModel):
    original: str = Field(..., description="Hatalı kullanılan kısım")
    correction: str = Field(..., description="Doğru biçim")
    error_type: str = Field(..., description="Gramer, Artikel, Sözdizimi, İmla, Kelime Seçimi")
    explanation_tr: str = Field(..., description="Hataya dair Türkçe açıklama ve kural")


class WritingAnalysisResponse(BaseModel):
    original_text: str
    target_level: str
    overall_score: int = Field(..., description="100 üzerinden verilen genel puan")
    assessed_level: str = Field(..., description="Metnin değerlendirilen seviyesi")
    corrected_text: str = Field(..., description="Hataları düzeltilmiş tam Almanca metin")
    errors: List[ErrorItem] = Field(default_factory=list, description="Bulunan hatalar ve açıklamaları")
    strengths: List[str] = Field(default_factory=list, description="Metindeki güçlü yönler")
    improvements: List[str] = Field(default_factory=list, description="Geliştirilmesi gereken noktalar")
    vocabulary_suggestions: List[Dict[str, str]] = Field(default_factory=list, description="Daha ileri düzey alternatif kelimeler")


# --- Konu Analizi & Özetleme Modelleri ---

class TopicSummaryRequest(BaseModel):
    topic: str
    level: Optional[GermanLevelEnum] = Field(GermanLevelEnum.A1)
    provider: AIProviderEnum = Field(AIProviderEnum.GEMINI)


class VocabularyItem(BaseModel):
    german: str
    turkish: str
    article: Optional[str] = None
    plural: Optional[str] = None


class SentenceExample(BaseModel):
    german: str
    turkish: str
    context_note: Optional[str] = None


class TopicSummaryResponse(BaseModel):
    topic: str
    level: str
    summary_tr: str
    key_grammar_rules: List[str] = Field(default_factory=list)
    vocabulary: List[VocabularyItem] = Field(default_factory=list)
    examples: List[SentenceExample] = Field(default_factory=list)
    common_mistakes: List[str] = Field(default_factory=list)
    mini_quiz: List[Dict[str, Any]] = Field(default_factory=list)


# --- İnteraktif Hikaye Modülü Modelleri ---

class StoryRequest(BaseModel):
    level: GermanLevelEnum = Field(GermanLevelEnum.A1)
    topic_theme: Optional[str] = Field("Günlük Yaşam")
    provider: AIProviderEnum = Field(AIProviderEnum.GEMINI)


class WordAnnotation(BaseModel):
    w: str
    tr: str
    type: Optional[str] = None
    article: Optional[str] = None
    plural: Optional[str] = None


class StoryParagraph(BaseModel):
    german_text: str
    words: List[WordAnnotation] = Field(default_factory=list)


class StoryResponse(BaseModel):
    title_de: str
    title_tr: str
    level: str
    paragraphs: List[StoryParagraph] = Field(default_factory=list)
    full_translation_tr: str
    key_vocabulary: List[VocabularyItem] = Field(default_factory=list)


# --- Fiil Çekimi Modelleri ---

class PersonalPronouns(BaseModel):
    ich: str
    du: str
    er_sie_es: str
    wir: str
    ihr: str
    sie_Sie: str


class TenseConjugation(BaseModel):
    tense_name: str
    turkish_tense_name: str
    forms: PersonalPronouns
    auxiliary_verb: Optional[str] = None


class VerbConjugationRequest(BaseModel):
    verb: str
    provider: AIProviderEnum = Field(AIProviderEnum.GEMINI)


class VerbConjugationResponse(BaseModel):
    verb: str
    turkish_meaning: str
    is_regular: bool
    auxiliary_verb: str
    stammformen: Optional[str] = None
    tenses: List[TenseConjugation] = Field(default_factory=list)
    example_sentences: List[SentenceExample] = Field(default_factory=list)


# --- Çeviri & Sözlük Modelleri ---

class TranslationRequest(BaseModel):
    text: str
    direction: TranslationDirectionEnum = Field(TranslationDirectionEnum.DE_TO_TR)
    provider: AIProviderEnum = Field(AIProviderEnum.GEMINI)


class DictionaryEntry(BaseModel):
    german: str
    turkish: str
    article: Optional[str] = None
    plural: Optional[str] = None
    word_type: Optional[str] = None
    phonetic: Optional[str] = None
    examples: List[SentenceExample] = Field(default_factory=list)
    synonyms: List[str] = Field(default_factory=list)
    grammar_tips: Optional[str] = None


class TranslationResponse(BaseModel):
    source_text: str
    direction: str
    main_translation: str
    dictionary_entry: Optional[DictionaryEntry] = None
    alternative_translations: List[str] = Field(default_factory=list)


class PDFExportRequest(BaseModel):
    title: str
    subtitle: Optional[str] = "Betül Altınkaynak Demirel - Yapay Zeka Destekli Almanca Öğrenme Raporu"
    content_markdown: str
    author: Optional[str] = "Betül Altınkaynak Demirel"
