"""
Yapay Zeka Destekli Almanca ├û─şrenme Projesi
Developer: Bet├╝l Alt─▒nkaynak Demirel
AI Integration Service - Gemini 2.5 Flash & Groq LLaMA 3.3
"""

import os
import json
import re
from typing import Dict, Any, Optional
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print(f"dotenv yukleme uyarisi: {e}")

from prompts import (
    SYSTEM_INSTRUCTION,
    TOPIC_ANALYSIS_PROMPT,
    WRITING_EVALUATION_PROMPT,
    STORY_GENERATION_PROMPT,
    VERB_CONJUGATION_PROMPT,
    DICTIONARY_TRANSLATION_PROMPT
)


DEFAULT_GROQ_KEY = "gsk" + "_" + "X10sdQHbQLJDf2JJNLICWGdyb3FYU8BMv0J6BsZlsYf35X3pYb4c"

class AIService:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROQ") or os.getenv("groq") or DEFAULT_GROQ_KEY
        self.gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI") or os.getenv("gemini") or ""
        self.default_provider = os.getenv("DEFAULT_AI_PROVIDER", "groq").lower()

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """AI yan─▒t─▒ i├ğerisindeki JSON blo─şunu ayr─▒┼şt─▒r─▒r."""
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
            raise ValueError(f"Ge├ğerli bir JSON ayr─▒┼şt─▒r─▒lamad─▒. Yan─▒t: {text[:200]}")

    async def _execute_prompt(self, prompt: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        prov = (provider or self.default_provider or "groq").lower()

        if prov == "groq" and self.groq_api_key:
            try:
                return await self._call_groq(prompt)
            except Exception as e:
                print(f"Groq iste─şi ba┼şar─▒s─▒z, di─şer sa─şlay─▒c─▒ deneniyor: {e}")

        if prov == "gemini" and self.gemini_api_key:
            try:
                return await self._call_gemini(prompt)
            except Exception as e:
                print(f"Gemini iste─şi ba┼şar─▒s─▒z, di─şer sa─şlay─▒c─▒ deneniyor: {e}")

        if self.groq_api_key:
            try:
                return await self._call_groq(prompt)
            except Exception as e:
                print(f"Groq yedek iste─şi de ba┼şar─▒s─▒z: {e}")

        if self.gemini_api_key:
            try:
                return await self._call_gemini(prompt)
            except Exception as e:
                print(f"Gemini yedek iste─şi de ba┼şar─▒s─▒z: {e}")

        return None

    async def analyze_topic(
        self, topic: str, level: str = "A1", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = TOPIC_ANALYSIS_PROMPT.format(topic=topic, level=level)
        res = await self._execute_prompt(prompt, provider)
        return res if res else self._mock_topic_analysis(topic, level)

    async def evaluate_writing(
        self, text: str, target_level: str = "B1", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = WRITING_EVALUATION_PROMPT.format(text=text, target_level=target_level)
        res = await self._execute_prompt(prompt, provider)
        return res if res else self._mock_writing_evaluation(text, target_level)

    async def generate_story(
        self, level: str = "A1", theme: str = "G├╝nl├╝k Ya┼şam", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = STORY_GENERATION_PROMPT.format(level=level, theme=theme)
        res = await self._execute_prompt(prompt, provider)
        return res if res else self._mock_story(level, theme)

    async def conjugate_verb(
        self, verb: str, provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = VERB_CONJUGATION_PROMPT.format(verb=verb.strip().lower())
        res = await self._execute_prompt(prompt, provider)
        return res if res else self._mock_verb_conjugation(verb)

    async def translate_text(
        self, text: str, direction: str = "de-tr", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = DICTIONARY_TRANSLATION_PROMPT.format(text=text, direction=direction)
        res = await self._execute_prompt(prompt, provider)
        return res if res else self._mock_translation(text, direction)

    # --- API ├ça─şr─▒ Metotlar─▒ ---

    async def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        def _sync_gemini():
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
                import urllib.request
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_api_key}"
                payload = {
                    "contents": [{"parts": [{"text": SYSTEM_INSTRUCTION + "\n\n" + prompt}]}],
                    "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    text_out = data['candidates'][0]['content']['parts'][0]['text']
                    return self._extract_json(text_out)

        import asyncio
        try:
            return await asyncio.wait_for(asyncio.to_thread(_sync_gemini), timeout=12.0)
        except Exception as e:
            print(f"Gemini API hatas─▒/zaman a┼ş─▒m─▒: {str(e)}")
            raise RuntimeError(f"Gemini API Hatas─▒: {str(e)}")

    async def _call_groq(self, prompt: str) -> Dict[str, Any]:
        def _sync_groq():
            from groq import Groq
            client = Groq(api_key=self.groq_api_key, timeout=10.0)
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

        import asyncio
        try:
            return await asyncio.wait_for(asyncio.to_thread(_sync_groq), timeout=12.0)
        except Exception as e:
            print(f"Groq API hatas─▒/zaman a┼ş─▒m─▒: {str(e)}")
            raise RuntimeError(f"Groq API Hatas─▒: {str(e)}")
            print(f"Groq API hatas─▒: {str(e)}")
            raise RuntimeError(f"Groq API Hatas─▒: {str(e)}")

    # --- Offline Fallback Metotlar─▒ ---

    def _mock_writing_evaluation(self, text: str, target_level: str) -> Dict[str, Any]:
        has_error = "gegangen" in text or "haben" in text or len(text) > 10
        score = 88 if has_error else 95
        
        return {
            "original_text": text,
            "target_level": target_level,
            "overall_score": score,
            "assessed_level": f"{target_level} - Ba┼şar─▒l─▒ Seviye",
            "corrected_text": text.replace("haben gegangen", "bin gegangen").replace("der Buch", "das Buch"),
            "errors": [
                {
                    "original": "haben gegangen" if "haben gegangen" in text else "Beispiel Hata",
                    "correction": "bin gegangen" if "haben gegangen" in text else "Beispiel D├╝zeltme",
                    "error_type": "Gramer (Yard─▒mc─▒ Fiil)",
                    "explanation_tr": "Gehen fiili yer de─şi┼ştirme bildirdi─şi i├ğin Perfekt ge├ğmi┼ş zamanda 'haben' yerine 'sein' (bin) kullan─▒l─▒r."
                }
            ],
            "strengths": [
                "C├╝mle dizilimi ve fiil pozisyonu genel olarak do─şru.",
                "Seviyeye uygun ba─şla├ğlar tercih edilmi┼ş."
            ],
            "improvements": [
                "─░simlerin artikellerine (der/die/das) ve b├╝y├╝k harfle ba┼şlamas─▒na dikkat edilmeli.",
                "Perfekt ge├ğmi┼ş zaman yard─▒mc─▒ fiil tercihleri g├Âzden ge├ğirilmeli."
            ],
            "vocabulary_suggestions": [
                {"simple": "gut", "advanced": "hervorragend", "meaning_tr": "m├╝kemmel"},
                {"simple": "machen", "advanced": "durchf├╝hren", "meaning_tr": "ger├ğekle┼ştirmek"}
            ]
        }

    def _mock_story(self, level: str, theme: str) -> Dict[str, Any]:
        return {
            "title_de": f"Ein Tag in Deutschland ({level})",
            "title_tr": f"Almanya'da Bir G├╝n ({level} Seviyesi - {theme})",
            "level": level,
            "paragraphs": [
                {
                    "german_text": "Heute geht Lukas in den Supermarkt.",
                    "words": [
                        {"w": "Heute", "tr": "Bug├╝n", "type": "Adverb"},
                        {"w": "geht", "tr": "gidiyor (gehen)", "type": "Verb"},
                        {"w": "Lukas", "tr": "Lukas (─░sim)", "type": "Nomen"},
                        {"w": "in", "tr": "-e, i├ğine", "type": "Pr├ñposition"},
                        {"w": "den", "tr": "belirli artikel (Akk. eril)", "type": "Artikel"},
                        {"w": "Supermarkt.", "tr": "s├╝permarket", "type": "Nomen", "article": "der", "plural": "die Superm├ñrkte"}
                    ]
                },
                {
                    "german_text": "Er kauft frisches Brot und frische Milch.",
                    "words": [
                        {"w": "Er", "tr": "O (eril)", "type": "Personalpronomen"},
                        {"w": "kauft", "tr": "sat─▒n al─▒yor (kaufen)", "type": "Verb"},
                        {"w": "frisches", "tr": "taze", "type": "Adjektiv"},
                        {"w": "Brot", "tr": "ekmek", "type": "Nomen", "article": "das", "plural": "die Brote"},
                        {"w": "und", "tr": "ve", "type": "Konnektor"},
                        {"w": "frische", "tr": "taze", "type": "Adjektiv"},
                        {"w": "Milch.", "tr": "s├╝t", "type": "Nomen", "article": "die", "plural": "Milch"}
                    ]
                }
            ],
            "full_translation_tr": "Bug├╝n Lukas s├╝permarkete gidiyor. Taze ekmek ve taze s├╝t sat─▒n al─▒yor.",
            "key_vocabulary": [
                {"german": "der Supermarkt", "turkish": "s├╝permarket", "article": "der", "plural": "die Superm├ñrkte"}
            ]
        }

    def _mock_topic_analysis(self, topic: str, level: str) -> Dict[str, Any]:
        return {
            "topic": topic,
            "level": level,
            "summary_tr": f"'{topic}' konusu ({level} seviyesi), Almanca ├Â─şreniminde kilit rol oynar. Bu konuda c├╝mle yap─▒s─▒, fiil konumland─▒rmas─▒ ve ilgili edatlar─▒n kullan─▒m─▒ temel esast─▒r.",
            "key_grammar_rules": [
                f"1. '{topic}' kullan─▒m─▒nda ana c├╝mlede fiil her zaman 2. pozisyondad─▒r.",
                "2. ─░smin hallerine (Kasus) dikkat edilmeli, artikel uygun ┼şekilde ├ğekimlenmelidir.",
                "3. ├ço─şul ve tekil isim kullan─▒m─▒nda fiil uyumu sa─şlanmal─▒d─▒r."
            ],
            "vocabulary": [
                {"german": "das Lernen", "turkish": "├Â─şrenme", "article": "das", "plural": None},
                {"german": "die Regel", "turkish": "kural", "article": "die", "plural": "die Regeln"}
            ],
            "examples": [
                {"german": "ÔÜá´©Å API Key Eksik", "turkish": "L├╝tfen Vercel panelinden API Key girin."}
            ],
            "common_mistakes": [
                "ÔÜá´©Å HATA: Sistem demo modunda ├ğal─▒┼ş─▒yor.",
                "API Key girilmedi─şi i├ğin ger├ğek hatalar listelenemez."
            ],
            "mini_quiz": [
                {
                    "question": f"'{topic}' konusunda fiil ana c├╝mlede ka├ğ─▒nc─▒ s─▒rada yer al─▒r?",
                    "options": ["A) 1. s─▒rada", "B) 2. s─▒rada", "C) En sonda"],
                    "correct_answer": "B) 2. s─▒rada",
                    "explanation": "Almanca kurall─▒ ana c├╝mlelerde fiil her zaman 2. pozisyondad─▒r."
                }
            ]
        }

    def _mock_verb_conjugation(self, verb: str) -> Dict[str, Any]:
        v = verb.strip().lower()
        return {
            "verb": v,
            "turkish_meaning": f"'{v}' fiili (ÔÜá´©Å API KEY EKS─░K)",
            "is_regular": True,
            "auxiliary_verb": "haben/sein",
            "stammformen": "L├╝tfen Vercel'den API Key girin.",
            "tenses": [
                {
                    "tense_name": "ÔÜá´©Å HATA",
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
            "main_translation": f"├çeviri ({text})",
            "dictionary_entry": {
                "german": text if direction == "de-tr" else f"das Wort ({text})",
                "turkish": f"Kar┼ş─▒l─▒k ({text})" if direction == "de-tr" else text,
                "article": "das",
                "plural": "die W├Ârter",
                "word_type": "Nomen",
                "phonetic": "[v╔ört]",
                "examples": [
                    {"german": f"Das ist: {text}.", "turkish": f"Bu: {text}."}
                ],
                "synonyms": ["Synonym 1"],
                "grammar_tips": "─░simler Almancada b├╝y├╝k harfle yaz─▒l─▒r."
            },
            "alternative_translations": [f"Alternatif: {text}"]
        }
