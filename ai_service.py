"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
AI Integration Service - Gemini 2.5 Flash & Groq LLaMA 3.3
"""

import os
import json
import re
from typing import Dict, Any, Optional
from fastapi import HTTPException

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Log presence of API keys (useful for debugging in Vercel logs)
if os.getenv("GROQ_API_KEY"):
    print("[DEBUG] GROQ_API_KEY found")
else:
    print("[DEBUG] GROQ_API_KEY NOT found")

if os.getenv("GEMINI_API_KEY"):
    print("[DEBUG] GEMINI_API_KEY found")
else:
    print("[DEBUG] GEMINI_API_KEY NOT found")

# Default keys (no placeholder, will be None if missing)
DEFAULT_GROQ_KEY = None

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
        self.groq_api_key = (os.getenv("GROQ_API_KEY") or os.getenv("GROQ") or os.getenv("groq") or DEFAULT_GROQ_KEY)
        if self.groq_api_key:
            self.groq_api_key = self.groq_api_key.strip()
        self.gemini_api_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI") or os.getenv("gemini") or "")
        if self.gemini_api_key:
            self.gemini_api_key = self.gemini_api_key.strip()
        self.default_provider = os.getenv("DEFAULT_AI_PROVIDER", "groq").lower()
        print(f"[DEBUG] Using Gemini model: {DEFAULT_GEMINI_MODEL}")

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

    async def _execute_prompt(self, prompt: str, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        # Verify that at least one API key is configured
        if not (self.gemini_api_key or self.groq_api_key):
            return None
        prov = (provider or self.default_provider or "groq").lower()

        if prov == "groq" and self.groq_api_key:
            try:
                return await self._call_groq(prompt)
            except Exception as e:
                print(f"Groq isteği başarısız, diğer sağlayıcı deneniyor: {e}")

        if prov == "gemini" and self.gemini_api_key:
            try:
                return await self._call_gemini(prompt)
            except Exception as e:
                print(f"Gemini isteği başarısız, diğer sağlayıcı deneniyor: {e}")

        if self.groq_api_key:
            try:
                return await self._call_groq(prompt)
            except Exception as e:
                print(f"Groq yedek isteği de başarısız: {e}")

        if self.gemini_api_key:
            try:
                return await self._call_gemini(prompt)
            except Exception as e:
                print(f"Gemini yedek isteği de başarısız: {e}")

        return None

    async def analyze_topic(
        self, topic: str, level: str = "A1", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = TOPIC_ANALYSIS_PROMPT.format(topic=topic, level=level)
        res = await self._execute_prompt(prompt, provider)
        return res if res else self._build_topic_analysis_fallback(topic, level)

    async def evaluate_writing(
        self, text: str, target_level: str = "B1", provider: Optional[str] = None
    ) -> Dict[str, Any]:
        prompt = WRITING_EVALUATION_PROMPT.format(text=text, target_level=target_level)
        res = await self._execute_prompt(prompt, provider)
        return res if res else self._mock_writing_evaluation(text, target_level)

    async def generate_story(
        self, level: str = "A1", theme: str = "Günlük Yaşam", provider: Optional[str] = None
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

    # --- API Çağrı Metotları ---

    async def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        def _sync_gemini():
            try:
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=self.gemini_api_key)
                response = client.models.generate_content(
                    model=DEFAULT_GEMINI_MODEL,
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
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{DEFAULT_GEMINI_MODEL}:generateContent?key={self.gemini_api_key}"
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
            print(f"Gemini API hatası/zaman aşımı: {str(e)}")
            raise RuntimeError(f"Gemini API Hatası: {str(e)}")

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
            msg = str(e).lower()
            if "exceeded" in msg or "quota" in msg or "limit" in msg:
                print("Groq token limit reached, falling back to mock.")
                raise RuntimeError("TokenExhausted")
            print(f"Groq API hatası/zaman aşımı: {str(e)}")
            raise RuntimeError(f"Groq API Hatası: {str(e)}")
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

    def _build_topic_analysis_fallback(self, topic: str, level: str) -> Dict[str, Any]:
        topic_text = topic.strip() or "Almanca konu"
        level_text = level.upper() if level else "A1"
        topic_lower = topic_text.lower()

        if "begrüßung" in topic_lower or "sich vorstellen" in topic_lower or "selam" in topic_lower or "tanıt" in topic_lower:
            summary = (
                f"'{topic_text}' konusu ({level_text} seviyesi), Almancada Selamlaşma ve kendini tanıtma becerilerinin temelidir. "
                "Bu konu, isim, meslek, yaş, memleket gibi temel bilgileri kısa ve anlaşılır cümlelerle ifade etmeyi öğretir."
            )
            grammar_rules = [
                "1. Selamlaşma cümlelerinde uygun hitap şekli ve nezaket ifadesi kullanılır.",
                "2. Kendini tanıtırken ich, heiße, komme, wohne gibi temel yapılar kullanılır.",
                "3. Basit soru ve cevap kalıpları günlük iletişim için çok önemlidir."
            ]
            examples = [
                {"german": "Hallo! Ich heiße Elif.", "turkish": "Merhaba! Ben Elif."},
                {"german": "Wie heißt du?", "turkish": "Adın ne?"},
                {"german": "Ich komme aus Istanbul.", "turkish": "İstanbul'dan geliyorum."}
            ]
        elif "artikel" in topic_lower or "article" in topic_lower:
            summary = (
                f"'{topic_text}' konusu ({level_text} seviyesi), Almancada isimlerin cinsiyetini ve doğru artikel kullanımını anlamak için temel bir konudur. "
                "Bu konu, der/die/das gibi belirleyicilerin doğru seçimini ve cümle içindeki işlevini kavramaya yardımcı olur."
            )
            grammar_rules = [
                "1. İsimlerin cinsiyetleri der, die, das ile doğru şekilde eşleştirilmelidir.",
                "2. Belirli ve belirsiz artikel kullanımı cümle anlamını etkiler.",
                "3. Sıfat ve isim birlikte kullanıldığında artikel değişebilir."
            ]
            examples = [
                {"german": "Der Hund läuft im Garten.", "turkish": "Köpek bahçede koşuyor."},
                {"german": "Die Katze sitzt auf dem Sofa.", "turkish": "Kedi koltukta oturuyor."},
                {"german": "Das Auto ist neu.", "turkish": "Araba yeni."}
            ]
        elif "perfekt" in topic_lower or "geçmiş" in topic_lower:
            summary = (
                f"'{topic_text}' konusu ({level_text} seviyesi), geçmiş zamanın nasıl kurulduğunu anlatır. "
                "Bu yapıda fiillerin Partizip II formu, yardımcı fiiller ve zaman kullanımı birlikte düşünülür."
            )
            grammar_rules = [
                "1. Perfekt yapısında haben veya sein yardımcı fiili kullanılır.",
                "2. Ana fiil Partizip II formunda gelir.",
                "3. Hareket fiilleri çoğunlukla sein, durum fiilleri ise haben ile kullanılır."
            ]
            examples = [
                {"german": "Ich habe gestern gearbeitet.", "turkish": "Dün çalıştım."},
                {"german": "Wir sind nach Hause gegangen.", "turkish": "Eve gittik."},
                {"german": "Sie hat das Buch gelesen.", "turkish": "O kitap okudu."}
            ]
        else:
            summary = (
                f"'{topic_text}' konusu ({level_text} seviyesi), Almanca öğreniminde temel bir yapı olarak ele alınır. "
                "Bu açıklama, konuya giriş, önemli kurallar, örnek cümleler ve sık yapılan hataları özetler."
            )
            grammar_rules = [
                f"1. '{topic_text}' konusu cümle dizilimi ve dil bilgisi açısından önemli bir kavramdır.",
                "2. Her cümlede bağlam ve fiil konumu göz önünde bulundurulmalıdır.",
                "3. Öğrenme sürecinde örnek cümleler üzerinden tekrar yapmak çok etkilidir."
            ]
            examples = [
                {"german": "Ich lerne Deutsch jeden Tag.", "turkish": "Her gün Almanca öğreniyorum."},
                {"german": "Das ist ein gutes Beispiel.", "turkish": "Bu iyi bir örnektir."},
                {"german": "Wir sprechen zusammen über das Thema.", "turkish": "Birlikte konu hakkında konuşuyoruz."}
            ]

        return {
            "topic": topic_text,
            "level": level_text,
            "summary_tr": summary,
            "key_grammar_rules": grammar_rules,
            "vocabulary": [
                {"german": "das Thema", "turkish": "konu", "article": "das", "plural": "die Themen"},
                {"german": "die Regel", "turkish": "kural", "article": "die", "plural": "die Regeln"},
                {"german": "das Beispiel", "turkish": "örnek", "article": "das", "plural": "die Beispiele"}
            ],
            "examples": examples,
            "common_mistakes": [
                "Örnek cümlelerde artikel ve kelime sırası karıştırılmamalıdır.",
                "Fiil çekimi ve bağlam uyumu gözden geçirilmeli."
            ],
            "mini_quiz": [
                {
                    "question": f"'{topic_text}' konusunu anlamak için en etkili yöntem hangisidir?",
                    "options": ["A) Sadece kelime ezberlemek", "B) Örnek cümlelerle çalışmak", "C) Sadece çeviri yapmak", "D) Her şeyi atlamak"],
                    "correct_answer": "B) Örnek cümlelerle çalışmak",
                    "explanation": "Örnek cümleler, yapıyı gerçek kullanım içinde görmeye yardımcı olur."
                },
                {
                    "question": f"'{topic_text}' konusunun en önemli kısmı hangisidir?",
                    "options": ["A) Sadece çeviri", "B) Kurallar ve örnekler", "C) Yalnızca sesli tekrar", "D) Sadece konuşma"],
                    "correct_answer": "B) Kurallar ve örnekler",
                    "explanation": "Kuralı örneklerle birlikte öğrenmek konuya hakim olmayı kolaylaştırır."
                },
                {
                    "question": "Bu tür bir konuda hangi yaklaşım en faydalıdır?",
                    "options": ["A) Sürekli tekrar", "B) Sadece kısa not almak", "C) Hiç pratik yapmamak", "D) Yalnızca dinlemek"],
                    "correct_answer": "A) Sürekli tekrar",
                    "explanation": "Tekrar, öğrendiğiniz yapıyı kalıcı hale getirir."
                },
                {
                    "question": "Konuyu daha iyi kavramak için ne yapılmalıdır?",
                    "options": ["A) Basit örneklerle ilerlemek", "B) Çok zor cümleler yazmak", "C) Her şeyi atlamak", "D) Yalnızca teorik bilgi almak"],
                    "correct_answer": "A) Basit örneklerle ilerlemek",
                    "explanation": "Basit örnekler, kavramın temellerini sağlamlaştırır."
                },
                {
                    "question": "Hangi ifade konu çalışmasında doğru bir yöntemdir?",
                    "options": ["A) Cümleleri yazıp kontrol etmek", "B) Yalnızca okumak", "C) Çok az tekrar", "D) Konuyu geçmek"],
                    "correct_answer": "A) Cümleleri yazıp kontrol etmek",
                    "explanation": "Yazma ve kontrol, öğrenilen yapının pekişmesini sağlar."
                }
            ]
        }

    def _mock_topic_analysis(self, topic: str, level: str) -> Dict[str, Any]:
        return self._build_topic_analysis_fallback(topic, level)

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
