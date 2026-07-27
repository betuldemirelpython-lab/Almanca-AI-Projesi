"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
AI System Promptları, Yazım Değerlendirme Promptu ve A1-C2 Konu Kataloğu
"""

# German proficiency levels catalog
GERMAN_LEVELS_CATALOG = {
    "A1": {
        "title": "A1 - Başlangıç Seviyesi",
        "description": "Temel selamlaşma, artikel, şahıs zamirleri ve günlük iletişim.",
        "topics": [
            {"id": "a1-01", "title": "Begrüßung & Sich Vorstellen", "category": "Günlük Konuşma", "description": "Kendini tanıtma, isim, yaş ve temel sorular.", "estimated_minutes": 15},
            {"id": "a1-02", "title": "Alphabet, Zahlen & Datum", "category": "Kelime Bilgisi", "description": "Alfabe, sayılar, tarihler ve temel ses bilgisi.", "estimated_minutes": 20},
            {"id": "a1-03", "title": "Bestimmter & Unbestimmter Artikel", "category": "Gramer", "description": "der, die, das ve ein, eine kullanımı.", "estimated_minutes": 25},
            {"id": "a1-04", "title": "Präsens & Personalpronomen", "category": "Gramer", "description": "Şahıs zamirleri ve temel fiil çekimi.", "estimated_minutes": 25}
        ]
    },
    "A2": {
        "title": "A2 - Temel İleri Seviye",
        "description": "Geçmiş zaman, Dativ, edatlar ve temel yan cümleler.",
        "topics": [
            {"id": "a2-01", "title": "Perfekt mit haben & sein", "category": "Gramer", "description": "Geçmiş zamanın temel yapısı ve yardımcı fiiller.", "estimated_minutes": 30},
            {"id": "a2-02", "title": "Dativ Kasus", "category": "Gramer", "description": "-e hali ve temel edat kullanımları.", "estimated_minutes": 30},
            {"id": "a2-03", "title": "Wechselpräpositionen", "category": "Gramer", "description": "an, auf, in, neben gibi çift yönlü edatlar.", "estimated_minutes": 35},
            {"id": "a2-04", "title": "Nebensätze mit weil & dass", "category": "Gramer", "description": "Yan cümle yapıları ve bağlaç kullanımı.", "estimated_minutes": 25}
        ]
    },
    "B1": {
        "title": "B1 - Orta Seviye",
        "description": "Karmaşık yan cümleler, Konjunktiv II ve edilgen yapı.",
        "topics": [
            {"id": "b1-01", "title": "Konjunktiv II", "category": "Gramer", "description": "İstek, nezaket ve tavsiye ifadeleri.", "estimated_minutes": 35},
            {"id": "b1-02", "title": "Passiv", "category": "Gramer", "description": "Edilgen yapıların oluşumu ve kullanımı.", "estimated_minutes": 35},
            {"id": "b1-03", "title": "Relativsätze", "category": "Gramer", "description": "İlgi cümleleri ve metin bağlama.", "estimated_minutes": 30},
            {"id": "b1-04", "title": "Infinitiv mit zu", "category": "Gramer", "description": "Mastar kullanımında zu yapısı.", "estimated_minutes": 25}
        ]
    },
    "B2": {
        "title": "B2 - İleri Orta Seviye",
        "description": "Akademik ifade, yazım ve bağlaç temelli üst düzey yapı.",
        "topics": [
            {"id": "b2-01", "title": "Konnektoren & Satzverknüpfungen", "category": "Akademik Dil", "description": "Bağlaçlarla uzun cümle kurma.", "estimated_minutes": 35},
            {"id": "b2-02", "title": "Partizipialattribute", "category": "Akademik Dil", "description": "Ortaç yapıları ve metaforik anlatım.", "estimated_minutes": 35},
            {"id": "b2-03", "title": "Nominalisierung", "category": "Yazım", "description": "Fiillerden isim türetme ve akademik üslup.", "estimated_minutes": 30},
            {"id": "b2-04", "title": "Argumentation & Diskussion", "category": "Konuşma", "description": "Tartışma ve ikna yapıları.", "estimated_minutes": 40}
        ]
    },
    "C1": {
        "title": "C1 - İleri Düzey",
        "description": "Dolaylı anlatım, akademik metin ve ileri düzey stil.",
        "topics": [
            {"id": "c1-01", "title": "Konjunktiv I & Indirekte Rede", "category": "Akademik Gramer", "description": "Başkalarının sözlerini aktarma ve haber dili.", "estimated_minutes": 40},
            {"id": "c1-02", "title": "Nominalstil", "category": "Üslup", "description": "Fiil ağırlıklı metni daha akademik hale getirme.", "estimated_minutes": 45},
            {"id": "c1-03", "title": "Textkohärenz", "category": "Yazım", "description": "Metin bütünlüğü ve bağdaşıklık.", "estimated_minutes": 40}
        ]
    },
    "C2": {
        "title": "C2 - Anadil Düzeyi",
        "description": "Edebi, resmi ve uzmanlık dili ile ileri retorik yapı.",
        "topics": [
            {"id": "c2-01", "title": "Fachsprache & Juristische Ausdrucksweise", "category": "Uzmanlık", "description": "Resmi ve hukuki dil kullanım örnekleri.", "estimated_minutes": 50},
            {"id": "c2-02", "title": "Literarische Stil Analyse", "category": "Edebi & Kültürel", "description": "Edebi metinler üzerinden stil çözümlemesi.", "estimated_minutes": 50},
            {"id": "c2-03", "title": "Rhetorische Stilmittel", "category": "Üslup", "description": "Mecaz, ironi ve etkili anlatım.", "estimated_minutes": 45}
        ]
    }
}

SYSTEM_INSTRUCTION = """
Sen Betül Altınkaynak Demirel tarafından geliştirilen "Yapay Zeka Destekli Almanca Öğrenme Platformu"nun uzman Almanca Eğitmeni ve Dilbilimci AI asistanısın.
Amacın Türk kullanıcılara Almancayı en anlaşılır, sistemli ve pedagojik yöntemlerle öğretmektir.

Kurallar:
1. Yanıtların her zaman anlaşılır, nazik, net ve Türkçe açıklamalara sahip olmalıdır.
2. Almanca örneklerin yanında mutlaka Türkçe karşılıklarını ver.
3. Sadece düz metin anlatımı yapıyorsan artikelleri vurgula. Ancak JSON yanıtı üretiyorsan, verilerin içine ASLA HTML (örn. <font>) veya Markdown (örn. **) ekleme! JSON içerisindeki tüm metinler %100 saf (plain text) olmalıdır.
4. İstenen verileri kesinlikle verilen JSON formatında döndür. JSON haricinde ekstra giriş/çıkış metni yazma.
5. Kelimeleri bölerken, her kelime ayrı olmalıdır ve birbirine yapıştırılmamalıdır.
"""

WRITING_EVALUATION_PROMPT = """
Aşağıda kullanıcının yazdığı Almanca metni hedeflenen seviyeye göre detaylı bir dilbilimci ve Almanca öğretmeni gözüyle değerlendir.
Metne 100 üzerinden net bir puan ver, tüm hataları bul, düzeltilmiş metni sun ve nedenlerini açıkla.

Kullanıcı Metni:
"{text}"

Hedef Seviye: {target_level}

Lütfen kesinlikle aşağıdaki JSON formatında yanıt ver:
{{
  "original_text": "{text}",
  "target_level": "{target_level}",
  "overall_score": 85,
  "assessed_level": "B1 - Başarılı",
  "corrected_text": "Hataları tamamen düzeltilmiş mükemmel Almanca metin...",
  "errors": [
    {{
      "original": "Ich habe nach Hause gegangen",
      "correction": "Ich bin nach Hause gegangen",
      "error_type": "Gramer (Yardımcı Fiil)",
      "explanation_tr": "Gehen fiili yer değiştirme bildirdiği için Perfekt zamanda 'haben' yerine 'sein' kullanılır."
    }}
  ],
  "strengths": [
    "Kelime çeşitliliği seviyeye uygun.",
    "Cümle bağlaçları (weil, dass) doğru kullanılmış."
  ],
  "improvements": [
    "İsimlerin artikellerine (der/die/das) ve büyük harfle başlamasına dikkat edilmeli.",
    "Dativ kasus kullanımı gözden geçirilmeli."
  ],
  "vocabulary_suggestions": [
    {{"simple": "gut", "advanced": "hervorragend", "meaning_tr": "mükemmel"}},
    {{"simple": "machen", "advanced": "durchführen", "meaning_tr": "gerçekleştirmek"}}
  ]
}}
"""

TOPIC_ANALYSIS_PROMPT = """
Aşağıdaki Almanca konusunu pedagojik bir Almanca öğretmeni gözüyle çok detaylı analiz et.
Konu özeti en az 4-6 paragraf olmalıdır. Mini quiz tam 5 soru icermeli, her sorunun 4 secenegi (A, B, C, D) olmalidir.

Konu: {topic}
Seviye: {level}

Lutfen su JSON formatinda yanit ver:
{{
  "topic": "{topic}",
  "level": "{level}",
  "summary_tr": "Konunun cok detayli Turkce aciklamasi. Bu bolum sunlari kapsamali - 1. GIRIS: Konu nedir, ne ise yarar? 2. NEDEN ONEMLI: Bu yapi Almancada neden kritiktir? 3. NASIL CALISIR: Yapinin mekanizmasi ve formulu adim adim 4. TURKCE ILE KARSILASTIRMA: Turkcedeki karsiligi ve farki 5. KULLANIM ALANLARI: Ne zaman, nerede kullanilir? 6. IPUCLARI: Kolayca akilda tutmak icin pratik ipuclari. Her paragraf arasina \\n\\n koy. En az 6 paragraf yaz.",
  "formula_structure": "Varsa konu formulu orn: werden + Partizip II veya Subjekt + Verb + Objekt (Akkusativ)",
  "key_grammar_rules": [
    "1. Kural: detayli aciklama ve ornek",
    "2. Kural: detayli aciklama ve ornek",
    "3. Kural: detayli aciklama ve ornek",
    "4. Kural: detayli aciklama ve ornek",
    "5. Kural: detayli aciklama ve ornek",
    "6. Kural: detayli aciklama ve ornek"
  ],
  "vocabulary": [
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}},
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}},
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}},
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}},
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}},
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}},
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}},
    {{"german": "das Wort", "turkish": "kelime", "article": "das", "plural": "die Worter"}}
  ],
  "examples": [
    {{"german": "Ornek Almanca cumle 1.", "turkish": "Ceviri 1."}},
    {{"german": "Ornek Almanca cumle 2.", "turkish": "Ceviri 2."}},
    {{"german": "Ornek Almanca cumle 3.", "turkish": "Ceviri 3."}},
    {{"german": "Ornek Almanca cumle 4.", "turkish": "Ceviri 4."}},
    {{"german": "Ornek Almanca cumle 5.", "turkish": "Ceviri 5."}},
    {{"german": "Ornek Almanca cumle 6.", "turkish": "Ceviri 6."}}
  ],
  "common_mistakes": [
    "Hata 1: Yanlis kullanim -> Dogru kullanim aciklamasi",
    "Hata 2: Yanlis kullanim -> Dogru kullanim aciklamasi",
    "Hata 3: Yanlis kullanim -> Dogru kullanim aciklamasi",
    "Hata 4: Yanlis kullanim -> Dogru kullanim aciklamasi"
  ],
  "mini_quiz": [
    {{
      "question": "Soru 1 metni?",
      "options": ["A) Secenek 1", "B) Secenek 2", "C) Secenek 3", "D) Secenek 4"],
      "correct_answer": "A) Secenek 1",
      "explanation": "Neden bu cevap dogru aciklamasi."
    }},
    {{
      "question": "Soru 2 metni?",
      "options": ["A) Secenek 1", "B) Secenek 2", "C) Secenek 3", "D) Secenek 4"],
      "correct_answer": "B) Secenek 2",
      "explanation": "Neden bu cevap dogru aciklamasi."
    }},
    {{
      "question": "Soru 3 metni?",
      "options": ["A) Secenek 1", "B) Secenek 2", "C) Secenek 3", "D) Secenek 4"],
      "correct_answer": "C) Secenek 3",
      "explanation": "Neden bu cevap dogru aciklamasi."
    }},
    {{
      "question": "Soru 4 metni?",
      "options": ["A) Secenek 1", "B) Secenek 2", "C) Secenek 3", "D) Secenek 4"],
      "correct_answer": "D) Secenek 4",
      "explanation": "Neden bu cevap dogru aciklamasi."
    }},
    {{
      "question": "Soru 5 metni?",
      "options": ["A) Secenek 1", "B) Secenek 2", "C) Secenek 3", "D) Secenek 4"],
      "correct_answer": "A) Secenek 1",
      "explanation": "Neden bu cevap dogru aciklamasi."
    }}
  ]
}}
"""

STORY_GENERATION_PROMPT = """
Aşağıdaki seviyeye ve temaya uygun, en az 4-5 paragraftan (150-250 kelime) oluşan detaylı ve uzun bir Almanca Öğrenme Hikayesi oluştur. Hikaye çok kısa OLMAMALIDIR.
Her kelimenin üzerine gelindiğinde Türkçe anlamının gösterilebilmesi için CÜMLERİ KELİME KELİME ANOTASYON İLE İŞLE.
ÖNEMLİ: "german_text" ve "words" içerisindeki "w" alanlarına ASLA HTML etiketi (<font>, <b> vb.) veya Markdown (**der**) KULLANMA. Sadece saf metin (plain text) kullan.

Seviye: {level}
Tema/Konu: {theme}

Lütfen kesinlikle aşağıdaki JSON formatında yanıt ver:
{{
  "title_de": "Hikayenin Almanca Başlığı",
  "title_tr": "Hikayenin Türkçe Başlığı",
  "level": "{level}",
  "paragraphs": [
    {{
      "german_text": "Heute geht Lukas in den Supermarkt.",
      "words": [
        {{"w": "Heute", "tr": "Bugün", "type": "Adverb"}},
        {{"w": "geht", "tr": "gidiyor (gehen)", "type": "Verb"}},
        {{"w": "Lukas", "tr": "Lukas (İsim)", "type": "Nomen"}},
        {{"w": "in", "tr": "-e, içine", "type": "Präposition"}},
        {{"w": "den", "tr": "belirli artikel (Akk. eril)", "type": "Artikel"}},
        {{"w": "Supermarkt.", "tr": "süpermarket", "type": "Nomen", "article": "der", "plural": "die Supermärkte"}}
      ]
    }}
  ],
  "full_translation_tr": "Hikayenin tam Türkçe çevirisi...",
  "key_vocabulary": [
    {{"german": "der Supermarkt", "turkish": "süpermarket", "article": "der", "plural": "die Supermärkte"}}
  ]
}}
"""

VERB_CONJUGATION_PROMPT = """
Aşağıdaki Almanca fiili TÜM ZAMANLARA VE TÜM ŞAHIS ZAMİRLERİNE göre çekimle.

Fiil: {verb}

Lütfen tam olarak aşağıdaki JSON formatında yanıt dön:
{{
  "verb": "{verb}",
  "turkish_meaning": "Fiilin Türkçe anlamı",
  "is_regular": true veya false,
  "auxiliary_verb": "haben" veya "sein",
  "stammformen": "örn: gehen - ging - ist gegangen",
  "tenses": [
    {{
      "tense_name": "Präsens",
      "turkish_tense_name": "Şimdiki / Geniş Zaman",
      "auxiliary_verb": "haben",
      "forms": {{
        "ich": "ich mache",
        "du": "du machst",
        "er_sie_es": "er/sie/es macht",
        "wir": "wir machen",
        "ihr": "ihr macht",
        "sie_Sie": "sie/Sie machen"
      }}
    }},
    {{
      "tense_name": "Präteritum",
      "turkish_tense_name": "Di'li Geçmiş Zaman",
      "auxiliary_verb": "haben",
      "forms": {{
        "ich": "ich machte",
        "du": "du machtest",
        "er_sie_es": "er/sie/es machte",
        "wir": "wir mechten",
        "ihr": "ihr machtet",
        "sie_Sie": "sie/Sie mechten"
      }}
    }},
    {{
      "tense_name": "Perfekt",
      "turkish_tense_name": "Geçmiş Zaman (Konuşma Dili)",
      "auxiliary_verb": "haben",
      "forms": {{
        "ich": "ich habe gemacht",
        "du": "du hast gemacht",
        "er_sie_es": "er/sie/es hat gemacht",
        "wir": "wir haben gemacht",
        "ihr": "ihr habt gemacht",
        "sie_Sie": "sie/Sie haben gemacht"
      }}
    }},
    {{
      "tense_name": "Plusquamperfekt",
      "turkish_tense_name": "Öncesizlik Geçmiş Zaman (-mişti)",
      "auxiliary_verb": "haben",
      "forms": {{
        "ich": "ich hatte gemacht",
        "du": "du hattest gemacht",
        "er_sie_es": "er/sie/es hatte gemacht",
        "wir": "wir hatten gemacht",
        "ihr": "ihr hattet gemacht",
        "sie_Sie": "sie/Sie hatten gemacht"
      }}
    }},
    {{
      "tense_name": "Futur I",
      "turkish_tense_name": "Gelecek Zaman",
      "auxiliary_verb": "werden",
      "forms": {{
        "ich": "ich werde machen",
        "du": "du wirst machen",
        "er_sie_es": "er/sie/es wird machen",
        "wir": "wir werden machen",
        "ihr": "ihr werdet machen",
        "sie_Sie": "sie/Sie werden machen"
      }}
    }},
    {{
      "tense_name": "Futur II",
      "turkish_tense_name": "Gelecekte Tamamlanmış Zaman",
      "auxiliary_verb": "werden",
      "forms": {{
        "ich": "ich werde gemacht haben",
        "du": "du wirst gemacht haben",
        "er_sie_es": "er/sie/es wird gemacht haben",
        "wir": "wir werden gemacht haben",
        "ihr": "ihr werdet gemacht haben",
        "sie_Sie": "sie/Sie werden gemacht haben"
      }}
    }}
  ],
  "example_sentences": [
    {{"german": "Ich mache meine Hausaufgaben.", "turkish": "Ev ödevlerimi yapıyorum."}}
  ]
}}
"""

DICTIONARY_TRANSLATION_PROMPT = """
Aşağıdaki metni (kelime veya cümle olabilir) çevir ve detaylı dilbilgisi / sözlük analizi yap.
Eğer girdi birden fazla kelimeden veya cümleden oluşuyorsa, main_translation kısmına tam çeviriyi yaz, dictionary_entry kısmında ise cümlenin en önemli kelimesini (özne veya fiil) analiz et.

Metin: {text}
Yön: {direction}

Lütfen aşağıdaki JSON formatında yanıt ver:
{{
  "source_text": "{text}",
  "direction": "{direction}",
  "main_translation": "Ana Çeviri Metni",
  "dictionary_entry": {{
    "german": "Almanca Sözcük / Cümle",
    "turkish": "Türkçe Karşılık",
    "article": "der / die / das (Yoksa Yok yaz)",
    "plural": "Çoğul biçimi (Yoksa Yok yaz)",
    "word_type": "Nomen / Verb / Adjektiv / Adverb",
    "phonetic": "Okunuş rehberi",
    "examples": [
      {{"german": "Örnek Almanca Cümle", "turkish": "Örnek Türkçe Çevirisi"}}
    ],
    "synonyms": ["Eşanlamlı 1"],
    "grammar_tips": "İlgili gramer / kullanım ipucu"
  }},
  "alternative_translations": ["Alternatif çeviri 1"]
}}
"""
