"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
AI System Promptları, Yazım Değerlendirme Promptu ve A1-C2 Konu Kataloğu
"""

SYSTEM_INSTRUCTION = """
Sen Betül Altınkaynak Demirel tarafından geliştirilen "Yapay Zeka Destekli Almanca Öğrenme Platformu"nun uzman Almanca Eğitmeni ve Dilbilimci AI asistanısın.
Amacın Türk kullanıcılara Almancayı en anlaşılır, sistemli ve pedagojik yöntemlerle öğretmektir.

Kurallar:
1. Yanıtların her zaman anlaşılır, nazik, net ve Türkçe açıklamalara sahip olmalıdır.
2. Almanca örneklerin yanında mutlaka Türkçe karşılıklarını ver.
3. Artikelleri (der/die/das) renk kodları ve net sembollerle vurgula (der = Eril, die = Dişil, das = Nötr).
4. İstenen verileri kesinlikle verilen JSON formatında döndür. JSON haricinde ekstra giriş/çıkış metni yazma.
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
Aşağıdaki Almanca konusunu ve seviyesini detaylı analiz et.

Konu: {topic}
Seviye: {level}

Lütfen şu JSON formatında yanıt ver:
{{
  "topic": "{topic}",
  "level": "{level}",
  "summary_tr": "Konunun detaylı Türkçe açıklaması ve mantığı...",
  "key_grammar_rules": [
    "Kural 1 açıklaması",
    "Kural 2 açıklaması"
  ],
  "vocabulary": [
    {{"german": "das Buch", "turkish": "kitap", "article": "das", "plural": "die Bücher"}}
  ],
  "examples": [
    {{"german": "Örnek 1...", "turkish": "Çeviri 1..."}},
    {{"german": "Örnek 2...", "turkish": "Çeviri 2..."}},
    {{"german": "Örnek 3...", "turkish": "Çeviri 3..."}}
  ],
  "common_mistakes": [
    "Konuya özel sık yapılan bir hata örneği (Lütfen aşağıdaki örneği kopyalama, konuya özgü üret!)",
    "Yanlış: [Yanlış Kullanım] -> Doğru: [Doğru Kullanım]"
  ],
  "mini_quiz": [
    {{
      "question": "Soru metni...",
      "options": ["A) Seçenek 1", "B) Seçenek 2"],
      "correct_answer": "A) Seçenek 1",
      "explanation": "Neden A şıkkı olduğu açıklaması..."
    }}
  ]
}}
"""

STORY_GENERATION_PROMPT = """
Aşağıdaki seviyeye ve temaya uygun kısa bir Almanca Öğrenme Hikayesi oluştur.
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
Metni çevir ve detaylı dilbilgisi / sözlük analizi yap.

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
    "article": "der / die / das",
    "plural": "Çoğul biçimi",
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

# --- EKSİKSİZ ALMANCA MÜFREDAT KATALOĞU ---
GERMAN_LEVELS_CATALOG = {
    "A1": {
        "title": "A1 - Başlangıç Seviyesi (Beginner)",
        "description": "Temel selamlaşma, artikeller, şahıs zamirleri, düzenli/düzensiz fiil çekimleri ve günlük iletişim.",
        "topics": [
            {"id": "a1-01", "title": "Begrüßung & Sich Vorstellen (Selamlaşma & Kendini Tanıtma)", "category": "Günlük Konuşma", "description": "Wie heißen Sie? Ich heiße... İsim, yaş, meslek ve memleket söyleme.", "estimated_minutes": 15},
            {"id": "a1-02", "title": "Alphabet, Zahlen & Datum (Almanca Harfler, Sayılar & Tarihler)", "category": "Kelime Bilgisi", "description": "Almanca alfabesi, Umlautlar (ä, ö, ü, ß), 1-1000 arası sayılar ve tarih okunuşu.", "estimated_minutes": 20},
            {"id": "a1-03", "title": "Bestimmter & Unbestimmter Artikel (Der, Die, Das & Ein, Eine)", "category": "Gramer", "description": "Almanca isimlerin cinsiyetleri (Eril, Dişil, Nötr) ve artikel mantığı.", "estimated_minutes": 25},
            {"id": "a1-04", "title": "Negationsartikel: kein & nicht (Olumsuzluk İfadeleri)", "category": "Gramer", "description": "İsim olumsuzlama (kein/keine) ve fiil/sıfat olumsuzlama (nicht) farkı.", "estimated_minutes": 20},
            {"id": "a1-05", "title": "Personalpronomen & Präsens Konjugation (Şahıs Zamirleri & Düzenli Fiil Çekimi)", "category": "Gramer", "description": "ich, du, er/sie/es, wir, ihr, sie/Sie zamirleri ve fiil köküne gelen -e, -st, -t, -en ekleri.", "estimated_minutes": 25},
            {"id": "a1-06", "title": "Unregelmäßige Verben: sein, haben, werden (Temel Düzensiz Fiiller)", "category": "Gramer", "description": "Almancanın en temel üç yardımcı fiilinin Präsens zamanındaki çekimleri.", "estimated_minutes": 20},
            {"id": "a1-07", "title": "Vokalwechsel Verben: e➔i, a➔ä (Kök Ünlüsü Değişen Fiiller)", "category": "Gramer", "description": "sprechen, lesen, sehen, fahren, schlafen fiillerinin du ve er/sie/es çekimleri.", "estimated_minutes": 20},
            {"id": "a1-08", "title": "W-Fragen & Ja/Nein-Fragen (Soru Cümleleri)", "category": "Cümle Kurulumu", "description": "Wer, Was, Wo, Wohin, Woher, Wie soru kelimeleri ve fiille başlayan sorular.", "estimated_minutes": 15},
            {"id": "a1-09", "title": "Pluralformen der Nomen (İsimlerin Çoğul Halleri)", "category": "Kelime Bilgisi", "description": "-e, -er, -en, -s takıları ve Umlaut alan çoğul isim yapıları.", "estimated_minutes": 20},
            {"id": "a1-10", "title": "Possessivpronomen im Nominativ (İyelik Zamirleri)", "category": "Gramer", "description": "mein, dein, sein, ihr, unser, euer, ihr/Ihr iyelik zamirlerinin kullanımı.", "estimated_minutes": 20},
            {"id": "a1-11", "title": "Akkusativ Kasus (-i Hali: den, einen, keinen)", "category": "Gramer", "description": "İsmin -i hali. Eril (der) artikelinin 'den / einen / keinen' olarak değişimi.", "estimated_minutes": 30},
            {"id": "a1-12", "title": "Imperativ im A1 (Emir Cümleleri)", "category": "Gramer", "description": "Komm!, Machen Sie!, Lernt! komut ve rica cümleleri.", "estimated_minutes": 15},
            {"id": "a1-13", "title": "Modalverben im A1: können, müssen, wollen (Temel Modal Fiiller)", "category": "Gramer", "description": "Ebilmek, zorunda olmak ve istemek fiillerinin kullanımı ve cümle sonu mastar kuralı.", "estimated_minutes": 25},
            {"id": "a1-14", "title": "Präpositionen: in, aus, nach, von, mit, zu (Temel Edatlar)", "category": "Gramer", "description": "Nereden (aus/von), nereye (nach/zu/in), neyle (mit) sorularına yanıt veren edatlar.", "estimated_minutes": 25},
            {"id": "a1-15", "title": "Tageszeiten, Wochentage & Uhrzeit (Saatler, Günler & Saat Sorma)", "category": "Günlük Konuşma", "description": "Wie spät ist es? Resmi ve gayriresmi saat okunuşları.", "estimated_minutes": 20}
        ]
    },
    "A2": {
        "title": "A2 - Temel İleri Seviye (Elementary)",
        "description": "Geçmiş zaman (Perfekt/Präteritum), Dativ, çift yönlü edatlar, modal fiiller ve sıfat çekimleri.",
        "topics": [
            {"id": "a2-01", "title": "Dativ Kasus (-e Hali: dem, der, den + n)", "category": "Gramer", "description": "İsmin -e hali. der➔dem, die➔der, das➔dem, die (plural)➔den + n değişimi.", "estimated_minutes": 30},
            {"id": "a2-02", "title": "Dativobjekt & Akkusativobjekt im Satz (Cümle İçi Nesne Dizilimi)", "category": "Gramer", "description": "Cümlede hem Dativ hem Akkusativ nesne olduğunda kelime sırası kuralları.", "estimated_minutes": 25},
            {"id": "a2-03", "title": "Wechselpräpositionen (Çift Yönlü Edatlar)", "category": "Gramer", "description": "an, auf, hinter, in, neben, über, unter, vor, zwischen + Akkusativ / Dativ.", "estimated_minutes": 35},
            {"id": "a2-04", "title": "Perfekt mit haben & sein (Konuşma Dilinde Geçmiş Zaman)", "category": "Gramer", "description": "Partizip II oluşumu ve ne zaman sein ne zaman haben yardımcı fiili kullanılır.", "estimated_minutes": 35},
            {"id": "a2-05", "title": "Partizip II Bildung (Geçmiş Zaman Sıfat-Fiil Oluşumu)", "category": "Gramer", "description": "Düzenli ge-t, düzensiz ge-en ve ayrılamayan fiillerin Partizip II halleri.", "estimated_minutes": 30},
            {"id": "a2-06", "title": "Präteritum der Hilfsverben & Modalverben (war, hatte, konnte, musste)", "category": "Gramer", "description": "sein, haben ve modal fiillerin Präteritum geçmiş zaman çekimleri.", "estimated_minutes": 25},
            {"id": "a2-07", "title": "Trennbare & Untrennbare Verben (Ayrılabilen & Ayrılamayan Fiiller)", "category": "Gramer", "description": "einkaufen, ankommen vs. verstehen, bekommen, empfehlen.", "estimated_minutes": 25},
            {"id": "a2-08", "title": "Reflexivverben im Akkusativ & Dativ (Dönüşlü Fiiller)", "category": "Gramer", "description": "sich freuen, sich waschen ve mich/mir zamirleri.", "estimated_minutes": 30},
            {"id": "a2-09", "title": "Modalverben im A2: dürfen, sollen, mögen / möchten", "category": "Gramer", "description": "İzin (dürfen), tavsiye (sollen) ve istek (möchten) ifadeleri.", "estimated_minutes": 25},
            {"id": "a2-10", "title": "Adjektivdeklination: Nominativ, Akkusativ, Dativ (Sıfat Çekimleri)", "category": "Gramer", "description": "Belirli ve belirsiz artikellerden sonra sıfat ekleri.", "estimated_minutes": 35},
            {"id": "a2-11", "title": "Komparativ & Superlativ (Sıfatlarda Derecelendirme)", "category": "Gramer", "description": "gut - besser - am besten karşılaştırma yapıları.", "estimated_minutes": 20},
            {"id": "a2-12", "title": "Nebensätze: weil, dass, wenn (Temel Yan Cümleler)", "category": "Gramer", "description": "Fiilin cümlenin en sonuna gittiği yan cümle bağlaçları.", "estimated_minutes": 30},
            {"id": "a2-13", "title": "Verben mit Dativ (Sadece Dativ Alan Fiiller)", "category": "Gramer", "description": "helfen, danken, gefällt, gehören, gratulieren fiilleri.", "estimated_minutes": 20},
            {"id": "a2-14", "title": "Dativ Personalpronomen (mir, dir, ihm, ihr, uns, euch, ihnen)", "category": "Gramer", "description": "Şahıs zamirlerinin Dativ (-e hali) çekimleri.", "estimated_minutes": 20},
            {"id": "a2-15", "title": "Zeitadverbien: gestern, heute, morgen, zuerst, dann, danach", "category": "Kelime Bilgisi", "description": "Zaman zarfları ve metin içinde olay sırası anlatma.", "estimated_minutes": 15}
        ]
    },
    "B1": {
        "title": "B1 - Orta Seviye (Intermediate / Goethe B1 / Telc B1)",
        "description": "Yan cümle bağlaçları, Konjunktiv II, Passiv, Relativsätze, Genitiv ve sınav hazırlığı.",
        "topics": [
            {"id": "b1-01", "title": "Nebensätze: obwohl, da, damit, um...zu (Karmaşık Yan Cümleler)", "category": "Gramer", "description": "Zıtlık, nedensellik ve amaç bağlaçları.", "estimated_minutes": 30},
            {"id": "b1-02", "title": "Konjunktiv II: Wunsch, Höflichkeit & Ratschlag (İstek & Nezaket)", "category": "Gramer", "description": "würde + Infinitiv, hätte, wäre yapısıyla ricalar.", "estimated_minutes": 35},
            {"id": "b1-03", "title": "Passiv im Präsens (Şimdiki Zamanda Edilgen Çatı)", "category": "Gramer", "description": "werden + Partizip II kullanımı.", "estimated_minutes": 35},
            {"id": "b1-04", "title": "Passiv im Präteritum & Perfekt (Geçmiş Zaman Edilgen Çatı)", "category": "Gramer", "description": "wurde + Partizip II ve ist + Partizip II + worden.", "estimated_minutes": 35},
            {"id": "b1-05", "title": "Relativsätze im Nominativ, Akkusativ, Dativ (İlgi Cümleleri)", "category": "Gramer", "description": "Der Mann, der dort steht... Nomen tanımlama.", "estimated_minutes": 30},
            {"id": "b1-06", "title": "Genitiv Kasus & Genitivpräpositionen (İsmin -in Hali)", "category": "Gramer", "description": "des, der artikelleri ve wegen, trotz, während edatları.", "estimated_minutes": 30},
            {"id": "b1-07", "title": "Indirekte Fragesätze: ob & W-Fragen (Dolaylı Soru Cümleleri)", "category": "Gramer", "description": "Ich weiß nicht, ob er kommt.", "estimated_minutes": 25},
            {"id": "b1-08", "title": "Finale Nebensätze: damit vs. um...zu (Amaç Cümleleri)", "category": "Gramer", "description": "Amaç belirten cümle yapıları.", "estimated_minutes": 25},
            {"id": "b1-09", "title": "Temporale Nebensätze: als, wenn, während, bevor, nachdem", "category": "Gramer", "description": "Zaman bağlaçları kullanımı.", "estimated_minutes": 30},
            {"id": "b1-10", "title": "Nomen-Verb-Verbindungen B1 (İsim-Fiil Kalıpları)", "category": "İş Almancası", "description": "Entscheidung treffen, Rolle spielen vb.", "estimated_minutes": 30},
            {"id": "b1-11", "title": "Infinitiv mit zu (zu ile Mastar Kullanımı)", "category": "Gramer", "description": "Es ist wichtig, zu lernen.", "estimated_minutes": 25},
            {"id": "b1-12", "title": "Futur I (Gelecek Zaman: werden + Infinitiv)", "category": "Gramer", "description": "Gelecek zaman ve tahmin cümleleri.", "estimated_minutes": 20},
            {"id": "b1-13", "title": "Plusquamperfekt (Geçmişin Geçmişi -mıştı Yapısı)", "category": "Gramer", "description": "hatte/war + Partizip II kullanımı.", "estimated_minutes": 25},
            {"id": "b1-14", "title": "Präteritum aller Verben (Yazılı Dilde Tüm Fiil Çekimleri)", "category": "Gramer", "description": "Hikaye ve haberlerde Präteritum biçimleri.", "estimated_minutes": 30},
            {"id": "b1-15", "title": "Adjektivdeklination im Genitiv & ohne Artikel (Karmaşık Sıfatlar)", "category": "Gramer", "description": "Artikelsiz isimlerin sıfat çekimleri.", "estimated_minutes": 25}
        ]
    },
    "B2": {
        "title": "B2 - İleri Orta Seviye (Vantage / Goethe B2)",
        "description": "Akademik Almanca, çift parçalı bağlaçlar, edilgen çatı alternatifleri, Partizip sıfatlar.",
        "topics": [
            {"id": "b2-01", "title": "Zweiteilige Konnektoren (İki Parçalı Bağlaçlar)", "category": "Gramer", "description": "sowohl... als auch, weder... noch vb.", "estimated_minutes": 30},
            {"id": "b2-02", "title": "Subjektlose Passivkonstruktionen & Passiversatzformen", "category": "İleri Gramer", "description": "sein + zu + Infinitiv, -bar/-lich ekleri.", "estimated_minutes": 35},
            {"id": "b2-03", "title": "Partizip I & Partizip II als Adjektiv (Sıfat Olarak Ortaçlar)", "category": "Akademik Dil", "description": "der lesende Student, das gelesene Buch.", "estimated_minutes": 35},
            {"id": "b2-04", "title": "Konjunktiv II in der Vergangenheit (Geçmişte İmkansız Koşul)", "category": "Gramer", "description": "hätte/wäre + Partizip II.", "estimated_minutes": 35},
            {"id": "b2-05", "title": "Genitivattribute & erweiterte Nomenphrasen (İleri Tamlamalar)", "category": "Akademik Dil", "description": "die Entwicklung des neuen Produkts...", "estimated_minutes": 30},
            {"id": "b2-06", "title": "Nomen-Verb-Verbindungen im Beruf & Wissenschaft", "category": "İş & Akademik", "description": "in Erwägung ziehen, zur Verfügung stehen.", "estimated_minutes": 40},
            {"id": "b2-07", "title": "Verben mit Präpositionalobjekt (Edatlı Fiiller)", "category": "Gramer", "description": "warten auf + Akk, sich interessieren für + Akk.", "estimated_minutes": 35},
            {"id": "b2-08", "title": "Präpositionalpronomen & Adverbien: worauf, darauf, wovon", "category": "Gramer", "description": "Edatlı zamirler ve nesne göndermeleri.", "estimated_minutes": 30},
            {"id": "b2-09", "title": "Irrealer Konditionalsatz ohne 'wenn' (wenn'siz Koşul)", "category": "Gramer", "description": "Hätte ich Zeit, käme ich zu dir.", "estimated_minutes": 25},
            {"id": "b2-10", "title": "Modale Partikeln (Vurgu Edatları: doch, ja, denn, halt)", "category": "Günlük & İleri Dil", "description": "Cümle içi vurgu kelimeleri.", "estimated_minutes": 30},
            {"id": "b2-11", "title": "Kausal-, Konzessiv-, Konditional- und Konsekutivsätze", "category": "Gramer", "description": "Karmaşık bağlaçların karşılaştırılması.", "estimated_minutes": 35},
            {"id": "b2-12", "title": "Nominalisierung von Verben und Adjektiven (İsimleştirme)", "category": "Akademik Yazım", "description": "das Reisen, das Schöne, beim Essen.", "estimated_minutes": 30},
            {"id": "b2-13", "title": "Wortbildung: Suffixe & Präfixe (-ung, -heit, ent-, ver-)", "category": "Kelime Bilgisi", "description": "Ön ve son takılarla kelime türetme.", "estimated_minutes": 30},
            {"id": "b2-14", "title": "Beschwerdebrief & Argumentation (Şikayet Mektubu & Argüman)", "category": "Yazım & Sınav", "description": "Resmi mektup ve argüman sunma şablonları.", "estimated_minutes": 40}
        ]
    },
    "C1": {
        "title": "C1 - İleri Düzey Yetkin Seviye (Effective Operational)",
        "description": "Konjunktiv I (Dolaylı anlatım), akademik metin dönüştürme, ortaç yapılar ve sunum dili.",
        "topics": [
            {"id": "c1-01", "title": "Konjunktiv I & Indirekte Rede (Dolaylı Anlatım / Haber Dili)", "category": "Akademik Gramer", "description": "Başkalarının sözlerini aktarma (er habe gesagt...).", "estimated_minutes": 40},
            {"id": "c1-02", "title": "Konjunktiv I Formbildung & Ersatzformen durch Konjunktiv II", "category": "Akademik Gramer", "description": "Präsens Konjunktiv I çekimleri.", "estimated_minutes": 35},
            {"id": "c1-03", "title": "Nominalstil vs. Verbalstil (Metin Üslubu Dönüştürme)", "category": "Üslup & Yazım", "description": "Fiil ağırlıklı metinleri akademik isim ağırlıklı metinlere dönüştürme.", "estimated_minutes": 45},
            {"id": "c1-04", "title": "Erweiterte Partizipialattribute (Genişletilmiş Ortaç Yapıları)", "category": "Akademik Dil", "description": "die seit Jahren in Deutschland arbeitenden Ingenieure.", "estimated_minutes": 45},
            {"id": "c1-05", "title": "Komplexe Satzgefüge & Satzverknüpfungen (Paragraf Bağlantıları)", "category": "Üslup", "description": "Akademik paragraflarda cümle geçişleri.", "estimated_minutes": 40},
            {"id": "c1-06", "title": "Modale Passiversatzformen: gehören + Partizip II, es gilt zu...", "category": "İleri Gramer", "description": "Das gehört verboten! Es gilt, Lösungen zu finden.", "estimated_minutes": 35},
            {"id": "c1-07", "title": "Nuancen der Modalpartikeln im C1 (İnce Vurgular)", "category": "Üslup", "description": "Cümledeki tonlamayı değiştiren kelimeler.", "estimated_minutes": 35},
            {"id": "c1-08", "title": "Wissenschaftliche Fachsprache & Textanalyse (Bilimsel Metin Analizi)", "category": "Uzmanlık", "description": "Makale ve tez okuma stratejileri.", "estimated_minutes": 50},
            {"id": "c1-09", "title": "Idiomatische Wendungen & Redensarten (İleri İdeomatik İfadeler)", "category": "Kelime Bilgisi", "description": "İleri düzey mecazi anlatımlar.", "estimated_minutes": 40},
            {"id": "c1-10", "title": "Redemittel für Diskussion, Debatte & Präsentation (Sunum Kalıpları)", "category": "Konuşma", "description": "Akademik tartışma ve ikna kalıpları.", "estimated_minutes": 45},
            {"id": "c1-11", "title": "Textkohärenz & Kohäsion (Metin Bütünlüğü ve Bağdaşıklık)", "category": "Yazım", "description": "Metin içi anlamsal uyum bağlaçları.", "estimated_minutes": 40},
            {"id": "c1-12", "title": "Feste Präposition-Nomen-Kombinationen (Sabit İsim-Edat Yapıları)", "category": "Gramer", "description": "in Bezug auf, im Zusammenhang mit...", "estimated_minutes": 40}
        ]
    },
    "C2": {
        "title": "C2 - Anadil Düzeyi Yetkinlik (Mastery / Goethe C2)",
        "description": "Edebi metinler, hukuki/resmi dil, retorik sanatlar, diyalektler ve anadil düzeyinde hakimiyet.",
        "topics": [
            {"id": "c2-01", "title": "Juristische & Amtliche Fachsprache (Resmi & Hukuki Almanca)", "category": "Uzmanlık", "description": "Sözleşme ve mahkeme kararları analizi.", "estimated_minutes": 50},
            {"id": "c2-02", "title": "Literarische Stilanalyse & Edebi Metin İncelemesi", "category": "Edebi & Kültürel", "description": "Kafka, Goethe metinleri üzerinden anlatım.", "estimated_minutes": 50},
            {"id": "c2-03", "title": "Rhetorische Stilmittel & Metaphern (Retorik Sanatlar & Mecazlar)", "category": "Üslup", "description": "Metapher, Ironie, Oxymoron retorik yapıları.", "estimated_minutes": 45},
            {"id": "c2-04", "title": "Ironie, Sarkasmus & Humor in der deutschen Sprache (Mizah ve İroni)", "category": "Kültürel Nüans", "description": "Alman kültüründe mizah ve ima.", "estimated_minutes": 45},
            {"id": "c2-05", "title": "Regionale Varietäten & Dialekte (Avusturya, İsviçre & Diyalektler)", "category": "Kültür & Dilbilim", "description": "Österreichisches Deutsch ve Schweizer Hochdeutsch.", "estimated_minutes": 45},
            {"id": "c2-06", "title": "Etymologie & Historische Grammatikentwicklung (Kelime Kökenleri)", "category": "Dilbilim", "description": "Almanca kelimelerin tarihsel kökeni ve evrimi.", "estimated_minutes": 50},
            {"id": "c2-07", "title": "Nuancenreiche Übersetzungstheorie DE-TR / TR-DE (Akademik Çeviri)", "category": "Çeviribilim", "description": "Metin türüne göre çeviri stratejileri.", "estimated_minutes": 50},
            {"id": "c2-08", "title": "Diplomatische & Verhandlungssprache (Üst Düzey Müzakere Dili)", "category": "Diplomasi & İletişim", "description": "Uluslararası ilişkiler ve müzakere söylemleri.", "estimated_minutes": 50}
        ]
    }
}
