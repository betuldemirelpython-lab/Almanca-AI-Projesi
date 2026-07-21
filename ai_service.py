"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
AI Integration Service - Gemini 2.5 Flash & Groq LLaMA 3.3
"""

import os
import json
import re
from typing import Dict, Any, Optional

from prompts import (
    SYSTEM_INSTRUCTION,
    TOPIC_ANALYSIS_PROMPT,
    WRITING_EVALUATION_PROMPT,
    STORY_GENERATION_PROMPT,
    VERB_CONJUGATION_PROMPT,
    DICTIONARY_TRANSLATION_PROMPT
)


class AIService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.default_provider = os.getenv("DEFAULT_AI_PROVIDER", "gemini").lower()

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """AI yanıtı içerisindeki JSON bloğunu ayrıştırır."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                return json.loads(text[start : end + 1])
            raise ValueError(f"Geçerli bir JSON ayrıştırılamadı. Yanıt: {text[:200]}")

    async def analyze_topic(
        self, topic: str, level: str = "A1", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prov = provider or self.default_provider
        prompt = TOPIC_ANALYSIS_PROMPT.format(topic=topic, level=level)

        if prov == "groq" and self.groq_api_key:
            return await self._call_groq(prompt)
        elif self.gemini_api_key:
            return await self._call_gemini(prompt)
        else:
            return self._mock_topic_analysis(topic, level)

    async def evaluate_writing(
        self, text: str, target_level: str = "B1", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """Kullanıcının yazdığı Almanca metni analiz eder, 100 üzerinden skorlar ve hatalarını düzeltir."""
        prov = provider or self.default_provider
        prompt = WRITING_EVALUATION_PROMPT.format(text=text, target_level=target_level)

        if prov == "groq" and self.groq_api_key:
            return await self._call_groq(prompt)
        elif self.gemini_api_key:
            return await self._call_gemini(prompt)
        else:
            return self._mock_writing_evaluation(text, target_level)

    async def generate_story(
        self, level: str = "A1", theme: str = "Günlük Yaşam", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prov = provider or self.default_provider
        prompt = STORY_GENERATION_PROMPT.format(level=level, theme=theme)

        if prov == "groq" and self.groq_api_key:
            return await self._call_groq(prompt)
        elif self.gemini_api_key:
            return await self._call_gemini(prompt)
        else:
            return self._mock_story(level, theme)

    async def conjugate_verb(
        self, verb: str, provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prov = provider or self.default_provider
        prompt = VERB_CONJUGATION_PROMPT.format(verb=verb.strip().lower())

        if prov == "groq" and self.groq_api_key:
            return await self._call_groq(prompt)
        elif self.gemini_api_key:
            return await self._call_gemini(prompt)
        else:
            return self._mock_verb_conjugation(verb)

    async def translate_text(
        self, text: str, direction: str = "de-tr", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prov = provider or self.default_provider
        prompt = DICTIONARY_TRANSLATION_PROMPT.format(text=text, direction=direction)

        if prov == "groq" and self.groq_api_key:
            return await self._call_groq(prompt)
        elif self.gemini_api_key:
            return await self._call_gemini(prompt)
        else:
            return self._mock_translation(text, direction)

    # --- API Çağrı Metotları ---

    async def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.gemini_api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.3,
                    response_mime_type="application/json",
                ),
            )
            return self._extract_json(response.text)
        except Exception as e:
            try:
                import urllib.request
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_api_key}"
                payload = {
                    "contents": [{"parts": [{"text": SYSTEM_INSTRUCTION + "\n\n" + prompt}]}],
                    "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    text_out = data['candidates'][0]['content']['parts'][0]['text']
                    return self._extract_json(text_out)
            except Exception as e_inner:
                print(f"Gemini API hatası: {str(e)} / {str(e_inner)}")
                raise RuntimeError(f"Gemini API Hatası: {str(e)}")

    async def _call_groq(self, prompt: str) -> Dict[str, Any]:
        try:
            from groq import Groq
            client = Groq(api_key=self.groq_api_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return self._extract_json(completion.choices[0].message.content)
        except Exception as e:
            print(f"Groq API hatası: {str(e)}")
            raise RuntimeError(f"Groq API Hatası: {str(e)}")

    # --- Offline Fallback Metotları ---

    def _mock_writing_evaluation(self, text: str, target_level: str) -> Dict[str, Any]:
        has_error = "gegangen" in text or "haben" in text or len(text) > 10
        score = 88 if has_error else 95
        
        return {
            "original_text": text,
            "target_level": target_level,
            "overall_score": score,
            "assessed_level": f"{target_level} - Başarılı Seviye",
            "corrected_text": text.replace("haben gegangen", "bin gegangen").replace("der Buch", "das Buch"),
            "errors": [
                {
                    "original": "haben gegangen" if "haben gegangen" in text else "Beispiel Hata",
                    "correction": "bin gegangen" if "haben gegangen" in text else "Beispiel Düzeltme",
                    "error_type": "Gramer (Yardımcı Fiil)",
                    "explanation_tr": "Gehen fiili yer değiştirme bildirdiği için Perfekt geçmiş zamanda 'haben' yerine 'sein' (bin) kullanılır."
                }
            ],
            "strengths": [
                "Cümle dizilimi ve fiil pozisyonu genel olarak doğru.",
                "Seviyeye uygun bağlaçlar tercih edilmiş."
            ],
            "improvements": [
                "İsimlerin artikellerine (der/die/das) ve büyük harfle başlamasına dikkat edilmeli.",
                "Perfekt geçmiş zaman yardımcı fiil tercihleri gözden geçirilmeli."
            ],
            "vocabulary_suggestions": [
                {"simple": "gut", "advanced": "hervorragend", "meaning_tr": "mükemmel"},
                {"simple": "machen", "advanced": "durchführen", "meaning_tr": "gerçekleştirmek"}
            ]
        }

    def _mock_story(self, level: str, theme: str) -> Dict[str, Any]:
        return {
            "title_de": f"Ein Tag in Deutschland ({level})",
            "title_tr": f"Almanya'da Bir Gün ({level} Seviyesi - {theme})",
            "level": level,
            "paragraphs": [
                {
                    "german_text": "Heute geht Lukas in den Supermarkt.",
                    "words": [
                        {"w": "Heute", "tr": "Bugün", "type": "Adverb"},
                        {"w": "geht", "tr": "gidiyor (gehen)", "type": "Verb"},
                        {"w": "Lukas", "tr": "Lukas (İsim)", "type": "Nomen"},
                        {"w": "in", "tr": "-e, içine", "type": "Präposition"},
                        {"w": "den", "tr": "belirli artikel (Akk. eril)", "type": "Artikel"},
                        {"w": "Supermarkt.", "tr": "süpermarket", "type": "Nomen", "article": "der", "plural": "die Supermärkte"}
                    ]
                },
                {
                    "german_text": "Er kauft frisches Brot und frische Milch.",
                    "words": [
                        {"w": "Er", "tr": "O (eril)", "type": "Personalpronomen"},
                        {"w": "kauft", "tr": "satın alıyor (kaufen)", "type": "Verb"},
                        {"w": "frisches", "tr": "taze", "type": "Adjektiv"},
                        {"w": "Brot", "tr": "ekmek", "type": "Nomen", "article": "das", "plural": "die Brote"},
                        {"w": "und", "tr": "ve", "type": "Konnektor"},
                        {"w": "frische", "tr": "taze", "type": "Adjektiv"},
                        {"w": "Milch.", "tr": "süt", "type": "Nomen", "article": "die", "plural": "Milch"}
                    ]
                }
            ],
            "full_translation_tr": "Bugün Lukas süpermarkete gidiyor. Taze ekmek ve taze süt satın alıyor.",
            "key_vocabulary": [
                {"german": "der Supermarkt", "turkish": "süpermarket", "article": "der", "plural": "die Supermärkte"}
            ]
        }

    def _mock_topic_analysis(self, topic: str, level: str) -> Dict[str, Any]:
        return {
            "topic": topic,
            "level": level,
            "summary_tr": f"'{topic}' konusu ({level} seviyesi), Almanca öğreniminde kilit rol oynar. Bu konuda cümle yapısı, fiil konumlandırması ve ilgili edatların kullanımı temel esastır.",
            "key_grammar_rules": [
                f"1. '{topic}' kullanımında ana cümlede fiil her zaman 2. pozisyondadır.",
                "2. İsmin hallerine (Kasus) dikkat edilmeli, artikel uygun şekilde çekimlenmelidir.",
                "3. Çoğul ve tekil isim kullanımında fiil uyumu sağlanmalıdır."
            ],
            "vocabulary": [
                {"german": "das Lernen", "turkish": "öğrenme", "article": "das", "plural": None},
                {"german": "die Regel", "turkish": "kural", "article": "die", "plural": "die Regeln"}
            ],
            "examples": [
                {"german": "⚠️ API Key Eksik", "turkish": "Lütfen Vercel panelinden API Key girin."}
            ],
            "common_mistakes": [
                "⚠️ HATA: Sistem demo modunda çalışıyor.",
                "API Key girilmediği için gerçek hatalar listelenemez."
            ],
            "mini_quiz": [
                {
                    "question": f"'{topic}' konusunda fiil ana cümlede kaçıncı sırada yer alır?",
                    "options": ["A) 1. sırada", "B) 2. sırada", "C) En sonda"],
                    "correct_answer": "B) 2. sırada",
                    "explanation": "Almanca kurallı ana cümlelerde fiil her zaman 2. pozisyondadır."
                }
            ]
        }

    def _mock_verb_conjugation(self, verb: str) -> Dict[str, Any]:
        v = verb.strip().lower()
        return {
            "verb": v,
            "turkish_meaning": f"'{v}' fiili (⚠️ API KEY EKSİK)",
            "is_regular": True,
            "auxiliary_verb": "haben/sein",
            "stammformen": "Lütfen Vercel'den API Key girin.",
            "tenses": [
                {
                    "tense_name": "⚠️ HATA",
                    "turkish_tense_name": "Sistem Demo Modunda",
                    "auxiliary_verb": "Yok",
                    "forms": {
                        "ich": "API Key Eksik",
                        "du": "API Key Eksik",
                        "er_sie_es": "API Key Eksik",
                        "wir": "API Key Eksik",
                        "ihr": "API Key Eksik",
                        "sie_Sie": "API Key Eksik"
                    }
                }
            ]
        }

    def _mock_translation(self, text: str, direction: str) -> Dict[str, Any]:
        return {
            "source_text": text,
            "direction": direction,
            "main_translation": f"Çeviri ({text})",
            "dictionary_entry": {
                "german": text if direction == "de-tr" else f"das Wort ({text})",
                "turkish": f"Karşılık ({text})" if direction == "de-tr" else text,
                "article": "das",
                "plural": "die Wörter",
                "word_type": "Nomen",
                "phonetic": "[vɔrt]",
                "examples": [
                    {"german": f"Das ist: {text}.", "turkish": f"Bu: {text}."}
                ],
                "synonyms": ["Synonym 1"],
                "grammar_tips": "İsimler Almancada büyük harfle yazılır."
            },
            "alternative_translations": [f"Alternatif: {text}"]
        }
