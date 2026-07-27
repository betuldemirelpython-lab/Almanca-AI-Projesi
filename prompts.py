"""
Yapay Zeka Destekli Almanca ├û─şrenme Projesi
Developer: Bet├╝l Alt─▒nkaynak Demirel
AI System Promptlar─▒, Yaz─▒m De─şerlendirme Promptu ve A1-C2 Konu Katalo─şu
"""

SYSTEM_INSTRUCTION = """
Sen Bet├╝l Alt─▒nkaynak Demirel taraf─▒ndan geli┼ştirilen "Yapay Zeka Destekli Almanca ├û─şrenme Platformu"nun uzman Almanca E─şitmeni ve Dilbilimci AI asistan─▒s─▒n.
Amac─▒n T├╝rk kullan─▒c─▒lara Almancay─▒ en anla┼ş─▒l─▒r, sistemli ve pedagojik y├Ântemlerle ├Â─şretmektir.

Kurallar:
1. Yan─▒tlar─▒n her zaman anla┼ş─▒l─▒r, nazik, net ve T├╝rk├ğe a├ğ─▒klamalara sahip olmal─▒d─▒r.
2. Almanca ├Ârneklerin yan─▒nda mutlaka T├╝rk├ğe kar┼ş─▒l─▒klar─▒n─▒ ver.
3. Sadece d├╝z metin anlat─▒m─▒ yap─▒yorsan artikelleri vurgula. Ancak JSON yan─▒t─▒ ├╝retiyorsan, verilerin i├ğine ASLA HTML (├Ârn. <font>) veya Markdown (├Ârn. **) ekleme! JSON i├ğerisindeki t├╝m metinler %100 saf (plain text) olmal─▒d─▒r.
4. ─░stenen verileri kesinlikle verilen JSON format─▒nda d├Ând├╝r. JSON haricinde ekstra giri┼ş/├ğ─▒k─▒┼ş metni yazma.
5. Kelimeleri b├Âlerken, her kelime ayr─▒ olmal─▒d─▒r ve birbirine yap─▒┼şt─▒r─▒lmamal─▒d─▒r.
"""

WRITING_EVALUATION_PROMPT = """
A┼şa─ş─▒da kullan─▒c─▒n─▒n yazd─▒─ş─▒ Almanca metni hedeflenen seviyeye g├Âre detayl─▒ bir dilbilimci ve Almanca ├Â─şretmeni g├Âz├╝yle de─şerlendir.
Metne 100 ├╝zerinden net bir puan ver, t├╝m hatalar─▒ bul, d├╝zeltilmi┼ş metni sun ve nedenlerini a├ğ─▒kla.

Kullan─▒c─▒ Metni:
"{text}"

Hedef Seviye: {target_level}

L├╝tfen kesinlikle a┼şa─ş─▒daki JSON format─▒nda yan─▒t ver:
{{
  "original_text": "{text}",
  "target_level": "{target_level}",
  "overall_score": 85,
  "assessed_level": "B1 - Ba┼şar─▒l─▒",
  "corrected_text": "Hatalar─▒ tamamen d├╝zeltilmi┼ş m├╝kemmel Almanca metin...",
  "errors": [
    {{
      "original": "Ich habe nach Hause gegangen",
      "correction": "Ich bin nach Hause gegangen",
      "error_type": "Gramer (Yard─▒mc─▒ Fiil)",
      "explanation_tr": "Gehen fiili yer de─şi┼ştirme bildirdi─şi i├ğin Perfekt zamanda 'haben' yerine 'sein' kullan─▒l─▒r."
    }}
  ],
  "strengths": [
    "Kelime ├ğe┼şitlili─şi seviyeye uygun.",
    "C├╝mle ba─şla├ğlar─▒ (weil, dass) do─şru kullan─▒lm─▒┼ş."
  ],
  "improvements": [
    "─░simlerin artikellerine (der/die/das) ve b├╝y├╝k harfle ba┼şlamas─▒na dikkat edilmeli.",
    "Dativ kasus kullan─▒m─▒ g├Âzden ge├ğirilmeli."
  ],
  "vocabulary_suggestions": [
    {{"simple": "gut", "advanced": "hervorragend", "meaning_tr": "m├╝kemmel"}},
    {{"simple": "machen", "advanced": "durchf├╝hren", "meaning_tr": "ger├ğekle┼ştirmek"}}
  ]
}}
"""

TOPIC_ANALYSIS_PROMPT = """
A┼şa─ş─▒daki Almanca konusunu ve seviyesini detayl─▒ analiz et.

Konu: {topic}
Seviye: {level}

L├╝tfen ┼şu JSON format─▒nda yan─▒t ver:
{{
  "topic": "{topic}",
  "level": "{level}",
  "summary_tr": "Konunun detayl─▒ T├╝rk├ğe a├ğ─▒klamas─▒ ve mant─▒─ş─▒...",
  "key_grammar_rules": [
    "Kural 1 a├ğ─▒klamas─▒",
    "Kural 2 a├ğ─▒klamas─▒"
  ],
  "vocabulary": [
    {{"german": "das Buch", "turkish": "kitap", "article": "das", "plural": "die B├╝cher"}}
  ],
  "examples": [
    {{"german": "├ûrnek 1...", "turkish": "├çeviri 1..."}},
    {{"german": "├ûrnek 2...", "turkish": "├çeviri 2..."}},
    {{"german": "├ûrnek 3...", "turkish": "├çeviri 3..."}}
  ],
  "common_mistakes": [
    "Konuya ├Âzel s─▒k yap─▒lan bir hata ├Ârne─şi (L├╝tfen a┼şa─ş─▒daki ├Ârne─şi kopyalama, konuya ├Âzg├╝ ├╝ret!)",
    "Yanl─▒┼ş: [Yanl─▒┼ş Kullan─▒m] -> Do─şru: [Do─şru Kullan─▒m]"
  ],
  "mini_quiz": [
    {{
      "question": "Soru metni...",
      "options": ["A) Se├ğenek 1", "B) Se├ğenek 2"],
      "correct_answer": "A) Se├ğenek 1",
      "explanation": "Neden A ┼ş─▒kk─▒ oldu─şu a├ğ─▒klamas─▒..."
    }}
  ]
}}
"""

STORY_GENERATION_PROMPT = """
A┼şa─ş─▒daki seviyeye ve temaya uygun, en az 4-5 paragraftan (150-250 kelime) olu┼şan detayl─▒ ve uzun bir Almanca ├û─şrenme Hikayesi olu┼ştur. Hikaye ├ğok k─▒sa OLMAMALIDIR.
Her kelimenin ├╝zerine gelindi─şinde T├╝rk├ğe anlam─▒n─▒n g├Âsterilebilmesi i├ğin C├£MLER─░ KEL─░ME KEL─░ME ANOTASYON ─░LE ─░┼ŞLE.
├ûNEML─░: "german_text" ve "words" i├ğerisindeki "w" alanlar─▒na ASLA HTML etiketi (<font>, <b> vb.) veya Markdown (**der**) KULLANMA. Sadece saf metin (plain text) kullan.

Seviye: {level}
Tema/Konu: {theme}

L├╝tfen kesinlikle a┼şa─ş─▒daki JSON format─▒nda yan─▒t ver:
{{
  "title_de": "Hikayenin Almanca Ba┼şl─▒─ş─▒",
  "title_tr": "Hikayenin T├╝rk├ğe Ba┼şl─▒─ş─▒",
  "level": "{level}",
  "paragraphs": [
    {{
      "german_text": "Heute geht Lukas in den Supermarkt.",
      "words": [
        {{"w": "Heute", "tr": "Bug├╝n", "type": "Adverb"}},
        {{"w": "geht", "tr": "gidiyor (gehen)", "type": "Verb"}},
        {{"w": "Lukas", "tr": "Lukas (─░sim)", "type": "Nomen"}},
        {{"w": "in", "tr": "-e, i├ğine", "type": "Pr├ñposition"}},
        {{"w": "den", "tr": "belirli artikel (Akk. eril)", "type": "Artikel"}},
        {{"w": "Supermarkt.", "tr": "s├╝permarket", "type": "Nomen", "article": "der", "plural": "die Superm├ñrkte"}}
      ]
    }}
  ],
  "full_translation_tr": "Hikayenin tam T├╝rk├ğe ├ğevirisi...",
  "key_vocabulary": [
    {{"german": "der Supermarkt", "turkish": "s├╝permarket", "article": "der", "plural": "die Superm├ñrkte"}}
  ]
}}
"""

VERB_CONJUGATION_PROMPT = """
A┼şa─ş─▒daki Almanca fiili T├£M ZAMANLARA VE T├£M ┼ŞAHIS ZAM─░RLER─░NE g├Âre ├ğekimle.

Fiil: {verb}

L├╝tfen tam olarak a┼şa─ş─▒daki JSON format─▒nda yan─▒t d├Ân:
{{
  "verb": "{verb}",
  "turkish_meaning": "Fiilin T├╝rk├ğe anlam─▒",
  "is_regular": true veya false,
  "auxiliary_verb": "haben" veya "sein",
  "stammformen": "├Ârn: gehen - ging - ist gegangen",
  "tenses": [
    {{
      "tense_name": "Pr├ñsens",
      "turkish_tense_name": "┼Şimdiki / Geni┼ş Zaman",
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
      "tense_name": "Pr├ñteritum",
      "turkish_tense_name": "Di'li Ge├ğmi┼ş Zaman",
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
      "turkish_tense_name": "Ge├ğmi┼ş Zaman (Konu┼şma Dili)",
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
      "turkish_tense_name": "├ûncesizlik Ge├ğmi┼ş Zaman (-mi┼şti)",
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
      "turkish_tense_name": "Gelecekte Tamamlanm─▒┼ş Zaman",
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
    {{"german": "Ich mache meine Hausaufgaben.", "turkish": "Ev ├Âdevlerimi yap─▒yorum."}}
  ]
}}
"""

DICTIONARY_TRANSLATION_PROMPT = """
A┼şa─ş─▒daki metni (kelime veya c├╝mle olabilir) ├ğevir ve detayl─▒ dilbilgisi / s├Âzl├╝k analizi yap.
E─şer girdi birden fazla kelimeden veya c├╝mleden olu┼şuyorsa, main_translation k─▒sm─▒na tam ├ğeviriyi yaz, dictionary_entry k─▒sm─▒nda ise c├╝mlenin en ├Ânemli kelimesini (├Âzne veya fiil) analiz et.

Metin: {text}
Y├Ân: {direction}

L├╝tfen a┼şa─ş─▒daki JSON format─▒nda yan─▒t ver:
{{
  "source_text": "{text}",
  "direction": "{direction}",
  "main_translation": "Ana ├çeviri Metni",
  "dictionary_entry": {{
    "german": "Almanca S├Âzc├╝k / C├╝mle",
    "turkish": "T├╝rk├ğe Kar┼ş─▒l─▒k",
    "article": "der / die / das (Yoksa Yok yaz)",
    "plural": "├ço─şul bi├ğimi (Yoksa Yok yaz)",
    "word_type": "Nomen / Verb / Adjektiv / Adverb",
    "phonetic": "Okunu┼ş rehberi",
    "examples": [
      {{"german": "├ûrnek Almanca C├╝mle", "turkish": "├ûrnek T├╝rk├ğe ├çevirisi"}}
    ],
    "synonyms": ["E┼şanlaml─▒ 1"],
    "grammar_tips": "─░lgili gramer / kullan─▒m ipucu"
  }},
  "alternative_translations": ["Alternatif ├ğeviri 1"]
}}
"""

# --- EKS─░KS─░Z ALMANCA M├£FREDAT KATALO─ŞU ---
GERMAN_LEVELS_CATALOG = {
    "A1": {
        "title": "A1 - Ba┼şlang─▒├ğ Seviyesi (Beginner)",
        "description": "Temel selamla┼şma, artikeller, ┼şah─▒s zamirleri, d├╝zenli/d├╝zensiz fiil ├ğekimleri ve g├╝nl├╝k ileti┼şim.",
        "topics": [
            {"id": "a1-01", "title": "Begr├╝├şung & Sich Vorstellen (Selamla┼şma & Kendini Tan─▒tma)", "category": "G├╝nl├╝k Konu┼şma", "description": "Wie hei├şen Sie? Ich hei├şe... ─░sim, ya┼ş, meslek ve memleket s├Âyleme.", "estimated_minutes": 15},
            {"id": "a1-02", "title": "Alphabet, Zahlen & Datum (Almanca Harfler, Say─▒lar & Tarihler)", "category": "Kelime Bilgisi", "description": "Almanca alfabesi, Umlautlar (├ñ, ├Â, ├╝, ├ş), 1-1000 aras─▒ say─▒lar ve tarih okunu┼şu.", "estimated_minutes": 20},
            {"id": "a1-03", "title": "Bestimmter & Unbestimmter Artikel (Der, Die, Das & Ein, Eine)", "category": "Gramer", "description": "Almanca isimlerin cinsiyetleri (Eril, Di┼şil, N├Âtr) ve artikel mant─▒─ş─▒.", "estimated_minutes": 25},
            {"id": "a1-04", "title": "Negationsartikel: kein & nicht (Olumsuzluk ─░fadeleri)", "category": "Gramer", "description": "─░sim olumsuzlama (kein/keine) ve fiil/s─▒fat olumsuzlama (nicht) fark─▒.", "estimated_minutes": 20},
            {"id": "a1-05", "title": "Personalpronomen & Pr├ñsens Konjugation (┼Şah─▒s Zamirleri & D├╝zenli Fiil ├çekimi)", "category": "Gramer", "description": "ich, du, er/sie/es, wir, ihr, sie/Sie zamirleri ve fiil k├Âk├╝ne gelen -e, -st, -t, -en ekleri.", "estimated_minutes": 25},
            {"id": "a1-06", "title": "Unregelm├ñ├şige Verben: sein, haben, werden (Temel D├╝zensiz Fiiller)", "category": "Gramer", "description": "Almancan─▒n en temel ├╝├ğ yard─▒mc─▒ fiilinin Pr├ñsens zaman─▒ndaki ├ğekimleri.", "estimated_minutes": 20},
            {"id": "a1-07", "title": "Vokalwechsel Verben: eÔŞöi, aÔŞö├ñ (K├Âk ├£nl├╝s├╝ De─şi┼şen Fiiller)", "category": "Gramer", "description": "sprechen, lesen, sehen, fahren, schlafen fiillerinin du ve er/sie/es ├ğekimleri.", "estimated_minutes": 20},
            {"id": "a1-08", "title": "W-Fragen & Ja/Nein-Fragen (Soru C├╝mleleri)", "category": "C├╝mle Kurulumu", "description": "Wer, Was, Wo, Wohin, Woher, Wie soru kelimeleri ve fiille ba┼şlayan sorular.", "estimated_minutes": 15},
            {"id": "a1-09", "title": "Pluralformen der Nomen (─░simlerin ├ço─şul Halleri)", "category": "Kelime Bilgisi", "description": "-e, -er, -en, -s tak─▒lar─▒ ve Umlaut alan ├ğo─şul isim yap─▒lar─▒.", "estimated_minutes": 20},
            {"id": "a1-10", "title": "Possessivpronomen im Nominativ (─░yelik Zamirleri)", "category": "Gramer", "description": "mein, dein, sein, ihr, unser, euer, ihr/Ihr iyelik zamirlerinin kullan─▒m─▒.", "estimated_minutes": 20},
            {"id": "a1-11", "title": "Akkusativ Kasus (-i Hali: den, einen, keinen)", "category": "Gramer", "description": "─░smin -i hali. Eril (der) artikelinin 'den / einen / keinen' olarak de─şi┼şimi.", "estimated_minutes": 30},
            {"id": "a1-12", "title": "Imperativ im A1 (Emir C├╝mleleri)", "category": "Gramer", "description": "Komm!, Machen Sie!, Lernt! komut ve rica c├╝mleleri.", "estimated_minutes": 15},
            {"id": "a1-13", "title": "Modalverben im A1: k├Ânnen, m├╝ssen, wollen (Temel Modal Fiiller)", "category": "Gramer", "description": "Ebilmek, zorunda olmak ve istemek fiillerinin kullan─▒m─▒ ve c├╝mle sonu mastar kural─▒.", "estimated_minutes": 25},
            {"id": "a1-14", "title": "Pr├ñpositionen: in, aus, nach, von, mit, zu (Temel Edatlar)", "category": "Gramer", "description": "Nereden (aus/von), nereye (nach/zu/in), neyle (mit) sorular─▒na yan─▒t veren edatlar.", "estimated_minutes": 25},
            {"id": "a1-15", "title": "Tageszeiten, Wochentage & Uhrzeit (Saatler, G├╝nler & Saat Sorma)", "category": "G├╝nl├╝k Konu┼şma", "description": "Wie sp├ñt ist es? Resmi ve gayriresmi saat okunu┼şlar─▒.", "estimated_minutes": 20}
        ]
    },
    "A2": {
        "title": "A2 - Temel ─░leri Seviye (Elementary)",
        "description": "Ge├ğmi┼ş zaman (Perfekt/Pr├ñteritum), Dativ, ├ğift y├Ânl├╝ edatlar, modal fiiller ve s─▒fat ├ğekimleri.",
        "topics": [
            {"id": "a2-01", "title": "Dativ Kasus (-e Hali: dem, der, den + n)", "category": "Gramer", "description": "─░smin -e hali. derÔŞödem, dieÔŞöder, dasÔŞödem, die (plural)ÔŞöden + n de─şi┼şimi.", "estimated_minutes": 30},
            {"id": "a2-02", "title": "Dativobjekt & Akkusativobjekt im Satz (C├╝mle ─░├ği Nesne Dizilimi)", "category": "Gramer", "description": "C├╝mlede hem Dativ hem Akkusativ nesne oldu─şunda kelime s─▒ras─▒ kurallar─▒.", "estimated_minutes": 25},
            {"id": "a2-03", "title": "Wechselpr├ñpositionen (├çift Y├Ânl├╝ Edatlar)", "category": "Gramer", "description": "an, auf, hinter, in, neben, ├╝ber, unter, vor, zwischen + Akkusativ / Dativ.", "estimated_minutes": 35},
            {"id": "a2-04", "title": "Perfekt mit haben & sein (Konu┼şma Dilinde Ge├ğmi┼ş Zaman)", "category": "Gramer", "description": "Partizip II olu┼şumu ve ne zaman sein ne zaman haben yard─▒mc─▒ fiili kullan─▒l─▒r.", "estimated_minutes": 35},
            {"id": "a2-05", "title": "Partizip II Bildung (Ge├ğmi┼ş Zaman S─▒fat-Fiil Olu┼şumu)", "category": "Gramer", "description": "D├╝zenli ge-t, d├╝zensiz ge-en ve ayr─▒lamayan fiillerin Partizip II halleri.", "estimated_minutes": 30},
            {"id": "a2-06", "title": "Pr├ñteritum der Hilfsverben & Modalverben (war, hatte, konnte, musste)", "category": "Gramer", "description": "sein, haben ve modal fiillerin Pr├ñteritum ge├ğmi┼ş zaman ├ğekimleri.", "estimated_minutes": 25},
            {"id": "a2-07", "title": "Trennbare & Untrennbare Verben (Ayr─▒labilen & Ayr─▒lamayan Fiiller)", "category": "Gramer", "description": "einkaufen, ankommen vs. verstehen, bekommen, empfehlen.", "estimated_minutes": 25},
            {"id": "a2-08", "title": "Reflexivverben im Akkusativ & Dativ (D├Ân├╝┼şl├╝ Fiiller)", "category": "Gramer", "description": "sich freuen, sich waschen ve mich/mir zamirleri.", "estimated_minutes": 30},
            {"id": "a2-09", "title": "Modalverben im A2: d├╝rfen, sollen, m├Âgen / m├Âchten", "category": "Gramer", "description": "─░zin (d├╝rfen), tavsiye (sollen) ve istek (m├Âchten) ifadeleri.", "estimated_minutes": 25},
            {"id": "a2-10", "title": "Adjektivdeklination: Nominativ, Akkusativ, Dativ (S─▒fat ├çekimleri)", "category": "Gramer", "description": "Belirli ve belirsiz artikellerden sonra s─▒fat ekleri.", "estimated_minutes": 35},
            {"id": "a2-11", "title": "Komparativ & Superlativ (S─▒fatlarda Derecelendirme)", "category": "Gramer", "description": "gut - besser - am besten kar┼ş─▒la┼şt─▒rma yap─▒lar─▒.", "estimated_minutes": 20},
            {"id": "a2-12", "title": "Nebens├ñtze: weil, dass, wenn (Temel Yan C├╝mleler)", "category": "Gramer", "description": "Fiilin c├╝mlenin en sonuna gitti─şi yan c├╝mle ba─şla├ğlar─▒.", "estimated_minutes": 30},
            {"id": "a2-13", "title": "Verben mit Dativ (Sadece Dativ Alan Fiiller)", "category": "Gramer", "description": "helfen, danken, gef├ñllt, geh├Âren, gratulieren fiilleri.", "estimated_minutes": 20},
            {"id": "a2-14", "title": "Dativ Personalpronomen (mir, dir, ihm, ihr, uns, euch, ihnen)", "category": "Gramer", "description": "┼Şah─▒s zamirlerinin Dativ (-e hali) ├ğekimleri.", "estimated_minutes": 20},
            {"id": "a2-15", "title": "Zeitadverbien: gestern, heute, morgen, zuerst, dann, danach", "category": "Kelime Bilgisi", "description": "Zaman zarflar─▒ ve metin i├ğinde olay s─▒ras─▒ anlatma.", "estimated_minutes": 15}
        ]
    },
    "B1": {
        "title": "B1 - Orta Seviye (Intermediate / Goethe B1 / Telc B1)",
        "description": "Yan c├╝mle ba─şla├ğlar─▒, Konjunktiv II, Passiv, Relativs├ñtze, Genitiv ve s─▒nav haz─▒rl─▒─ş─▒.",
        "topics": [
            {"id": "b1-01", "title": "Nebens├ñtze: obwohl, da, damit, um...zu (Karma┼ş─▒k Yan C├╝mleler)", "category": "Gramer", "description": "Z─▒tl─▒k, nedensellik ve ama├ğ ba─şla├ğlar─▒.", "estimated_minutes": 30},
            {"id": "b1-02", "title": "Konjunktiv II: Wunsch, H├Âflichkeit & Ratschlag (─░stek & Nezaket)", "category": "Gramer", "description": "w├╝rde + Infinitiv, h├ñtte, w├ñre yap─▒s─▒yla ricalar.", "estimated_minutes": 35},
            {"id": "b1-03", "title": "Passiv im Pr├ñsens (┼Şimdiki Zamanda Edilgen ├çat─▒)", "category": "Gramer", "description": "werden + Partizip II kullan─▒m─▒.", "estimated_minutes": 35},
            {"id": "b1-04", "title": "Passiv im Pr├ñteritum & Perfekt (Ge├ğmi┼ş Zaman Edilgen ├çat─▒)", "category": "Gramer", "description": "wurde + Partizip II ve ist + Partizip II + worden.", "estimated_minutes": 35},
            {"id": "b1-05", "title": "Relativs├ñtze im Nominativ, Akkusativ, Dativ (─░lgi C├╝mleleri)", "category": "Gramer", "description": "Der Mann, der dort steht... Nomen tan─▒mlama.", "estimated_minutes": 30},
            {"id": "b1-06", "title": "Genitiv Kasus & Genitivpr├ñpositionen (─░smin -in Hali)", "category": "Gramer", "description": "des, der artikelleri ve wegen, trotz, w├ñhrend edatlar─▒.", "estimated_minutes": 30},
            {"id": "b1-07", "title": "Indirekte Frages├ñtze: ob & W-Fragen (Dolayl─▒ Soru C├╝mleleri)", "category": "Gramer", "description": "Ich wei├ş nicht, ob er kommt.", "estimated_minutes": 25},
            {"id": "b1-08", "title": "Finale Nebens├ñtze: damit vs. um...zu (Ama├ğ C├╝mleleri)", "category": "Gramer", "description": "Ama├ğ belirten c├╝mle yap─▒lar─▒.", "estimated_minutes": 25},
            {"id": "b1-09", "title": "Temporale Nebens├ñtze: als, wenn, w├ñhrend, bevor, nachdem", "category": "Gramer", "description": "Zaman ba─şla├ğlar─▒ kullan─▒m─▒.", "estimated_minutes": 30},
            {"id": "b1-10", "title": "Nomen-Verb-Verbindungen B1 (─░sim-Fiil Kal─▒plar─▒)", "category": "─░┼ş Almancas─▒", "description": "Entscheidung treffen, Rolle spielen vb.", "estimated_minutes": 30},
            {"id": "b1-11", "title": "Infinitiv mit zu (zu ile Mastar Kullan─▒m─▒)", "category": "Gramer", "description": "Es ist wichtig, zu lernen.", "estimated_minutes": 25},
            {"id": "b1-12", "title": "Futur I (Gelecek Zaman: werden + Infinitiv)", "category": "Gramer", "description": "Gelecek zaman ve tahmin c├╝mleleri.", "estimated_minutes": 20},
            {"id": "b1-13", "title": "Plusquamperfekt (Ge├ğmi┼şin Ge├ğmi┼şi -m─▒┼şt─▒ Yap─▒s─▒)", "category": "Gramer", "description": "hatte/war + Partizip II kullan─▒m─▒.", "estimated_minutes": 25},
            {"id": "b1-14", "title": "Pr├ñteritum aller Verben (Yaz─▒l─▒ Dilde T├╝m Fiil ├çekimleri)", "category": "Gramer", "description": "Hikaye ve haberlerde Pr├ñteritum bi├ğimleri.", "estimated_minutes": 30},
            {"id": "b1-15", "title": "Adjektivdeklination im Genitiv & ohne Artikel (Karma┼ş─▒k S─▒fatlar)", "category": "Gramer", "description": "Artikelsiz isimlerin s─▒fat ├ğekimleri.", "estimated_minutes": 25}
        ]
    },
    "B2": {
        "title": "B2 - ─░leri Orta Seviye (Vantage / Goethe B2)",
        "description": "Akademik Almanca, ├ğift par├ğal─▒ ba─şla├ğlar, edilgen ├ğat─▒ alternatifleri, Partizip s─▒fatlar.",
        "topics": [
            {"id": "b2-01", "title": "Zweiteilige Konnektoren (─░ki Par├ğal─▒ Ba─şla├ğlar)", "category": "Gramer", "description": "sowohl... als auch, weder... noch vb.", "estimated_minutes": 30},
            {"id": "b2-02", "title": "Subjektlose Passivkonstruktionen & Passiversatzformen", "category": "─░leri Gramer", "description": "sein + zu + Infinitiv, -bar/-lich ekleri.", "estimated_minutes": 35},
            {"id": "b2-03", "title": "Partizip I & Partizip II als Adjektiv (S─▒fat Olarak Orta├ğlar)", "category": "Akademik Dil", "description": "der lesende Student, das gelesene Buch.", "estimated_minutes": 35},
            {"id": "b2-04", "title": "Konjunktiv II in der Vergangenheit (Ge├ğmi┼şte ─░mkans─▒z Ko┼şul)", "category": "Gramer", "description": "h├ñtte/w├ñre + Partizip II.", "estimated_minutes": 35},
            {"id": "b2-05", "title": "Genitivattribute & erweiterte Nomenphrasen (─░leri Tamlamalar)", "category": "Akademik Dil", "description": "die Entwicklung des neuen Produkts...", "estimated_minutes": 30},
            {"id": "b2-06", "title": "Nomen-Verb-Verbindungen im Beruf & Wissenschaft", "category": "─░┼ş & Akademik", "description": "in Erw├ñgung ziehen, zur Verf├╝gung stehen.", "estimated_minutes": 40},
            {"id": "b2-07", "title": "Verben mit Pr├ñpositionalobjekt (Edatl─▒ Fiiller)", "category": "Gramer", "description": "warten auf + Akk, sich interessieren f├╝r + Akk.", "estimated_minutes": 35},
            {"id": "b2-08", "title": "Pr├ñpositionalpronomen & Adverbien: worauf, darauf, wovon", "category": "Gramer", "description": "Edatl─▒ zamirler ve nesne g├Ândermeleri.", "estimated_minutes": 30},
            {"id": "b2-09", "title": "Irrealer Konditionalsatz ohne 'wenn' (wenn'siz Ko┼şul)", "category": "Gramer", "description": "H├ñtte ich Zeit, k├ñme ich zu dir.", "estimated_minutes": 25},
            {"id": "b2-10", "title": "Modale Partikeln (Vurgu Edatlar─▒: doch, ja, denn, halt)", "category": "G├╝nl├╝k & ─░leri Dil", "description": "C├╝mle i├ği vurgu kelimeleri.", "estimated_minutes": 30},
            {"id": "b2-11", "title": "Kausal-, Konzessiv-, Konditional- und Konsekutivs├ñtze", "category": "Gramer", "description": "Karma┼ş─▒k ba─şla├ğlar─▒n kar┼ş─▒la┼şt─▒r─▒lmas─▒.", "estimated_minutes": 35},
            {"id": "b2-12", "title": "Nominalisierung von Verben und Adjektiven (─░simle┼ştirme)", "category": "Akademik Yaz─▒m", "description": "das Reisen, das Sch├Âne, beim Essen.", "estimated_minutes": 30},
            {"id": "b2-13", "title": "Wortbildung: Suffixe & Pr├ñfixe (-ung, -heit, ent-, ver-)", "category": "Kelime Bilgisi", "description": "├ûn ve son tak─▒larla kelime t├╝retme.", "estimated_minutes": 30},
            {"id": "b2-14", "title": "Beschwerdebrief & Argumentation (┼Şikayet Mektubu & Arg├╝man)", "category": "Yaz─▒m & S─▒nav", "description": "Resmi mektup ve arg├╝man sunma ┼şablonlar─▒.", "estimated_minutes": 40}
        ]
    },
    "C1": {
        "title": "C1 - ─░leri D├╝zey Yetkin Seviye (Effective Operational)",
        "description": "Konjunktiv I (Dolayl─▒ anlat─▒m), akademik metin d├Ân├╝┼şt├╝rme, orta├ğ yap─▒lar ve sunum dili.",
        "topics": [
            {"id": "c1-01", "title": "Konjunktiv I & Indirekte Rede (Dolayl─▒ Anlat─▒m / Haber Dili)", "category": "Akademik Gramer", "description": "Ba┼şkalar─▒n─▒n s├Âzlerini aktarma (er habe gesagt...).", "estimated_minutes": 40},
            {"id": "c1-02", "title": "Konjunktiv I Formbildung & Ersatzformen durch Konjunktiv II", "category": "Akademik Gramer", "description": "Pr├ñsens Konjunktiv I ├ğekimleri.", "estimated_minutes": 35},
            {"id": "c1-03", "title": "Nominalstil vs. Verbalstil (Metin ├£slubu D├Ân├╝┼şt├╝rme)", "category": "├£slup & Yaz─▒m", "description": "Fiil a─ş─▒rl─▒kl─▒ metinleri akademik isim a─ş─▒rl─▒kl─▒ metinlere d├Ân├╝┼şt├╝rme.", "estimated_minutes": 45},
            {"id": "c1-04", "title": "Erweiterte Partizipialattribute (Geni┼şletilmi┼ş Orta├ğ Yap─▒lar─▒)", "category": "Akademik Dil", "description": "die seit Jahren in Deutschland arbeitenden Ingenieure.", "estimated_minutes": 45},
            {"id": "c1-05", "title": "Komplexe Satzgef├╝ge & Satzverkn├╝pfungen (Paragraf Ba─şlant─▒lar─▒)", "category": "├£slup", "description": "Akademik paragraflarda c├╝mle ge├ği┼şleri.", "estimated_minutes": 40},
            {"id": "c1-06", "title": "Modale Passiversatzformen: geh├Âren + Partizip II, es gilt zu...", "category": "─░leri Gramer", "description": "Das geh├Ârt verboten! Es gilt, L├Âsungen zu finden.", "estimated_minutes": 35},
            {"id": "c1-07", "title": "Nuancen der Modalpartikeln im C1 (─░nce Vurgular)", "category": "├£slup", "description": "C├╝mledeki tonlamay─▒ de─şi┼ştiren kelimeler.", "estimated_minutes": 35},
            {"id": "c1-08", "title": "Wissenschaftliche Fachsprache & Textanalyse (Bilimsel Metin Analizi)", "category": "Uzmanl─▒k", "description": "Makale ve tez okuma stratejileri.", "estimated_minutes": 50},
            {"id": "c1-09", "title": "Idiomatische Wendungen & Redensarten (─░leri ─░deomatik ─░fadeler)", "category": "Kelime Bilgisi", "description": "─░leri d├╝zey mecazi anlat─▒mlar.", "estimated_minutes": 40},
            {"id": "c1-10", "title": "Redemittel f├╝r Diskussion, Debatte & Pr├ñsentation (Sunum Kal─▒plar─▒)", "category": "Konu┼şma", "description": "Akademik tart─▒┼şma ve ikna kal─▒plar─▒.", "estimated_minutes": 45},
            {"id": "c1-11", "title": "Textkoh├ñrenz & Koh├ñsion (Metin B├╝t├╝nl├╝─ş├╝ ve Ba─şda┼ş─▒kl─▒k)", "category": "Yaz─▒m", "description": "Metin i├ği anlamsal uyum ba─şla├ğlar─▒.", "estimated_minutes": 40},
            {"id": "c1-12", "title": "Feste Pr├ñposition-Nomen-Kombinationen (Sabit ─░sim-Edat Yap─▒lar─▒)", "category": "Gramer", "description": "in Bezug auf, im Zusammenhang mit...", "estimated_minutes": 40}
        ]
    },
    "C2": {
        "title": "C2 - Anadil D├╝zeyi Yetkinlik (Mastery / Goethe C2)",
        "description": "Edebi metinler, hukuki/resmi dil, retorik sanatlar, diyalektler ve anadil d├╝zeyinde hakimiyet.",
        "topics": [
            {"id": "c2-01", "title": "Juristische & Amtliche Fachsprache (Resmi & Hukuki Almanca)", "category": "Uzmanl─▒k", "description": "S├Âzle┼şme ve mahkeme kararlar─▒ analizi.", "estimated_minutes": 50},
            {"id": "c2-02", "title": "Literarische Stilanalyse & Edebi Metin ─░ncelemesi", "category": "Edebi & K├╝lt├╝rel", "description": "Kafka, Goethe metinleri ├╝zerinden anlat─▒m.", "estimated_minutes": 50},
            {"id": "c2-03", "title": "Rhetorische Stilmittel & Metaphern (Retorik Sanatlar & Mecazlar)", "category": "├£slup", "description": "Metapher, Ironie, Oxymoron retorik yap─▒lar─▒.", "estimated_minutes": 45},
            {"id": "c2-04", "title": "Ironie, Sarkasmus & Humor in der deutschen Sprache (Mizah ve ─░roni)", "category": "K├╝lt├╝rel N├╝ans", "description": "Alman k├╝lt├╝r├╝nde mizah ve ima.", "estimated_minutes": 45},
            {"id": "c2-05", "title": "Regionale Variet├ñten & Dialekte (Avusturya, ─░svi├ğre & Diyalektler)", "category": "K├╝lt├╝r & Dilbilim", "description": "├ûsterreichisches Deutsch ve Schweizer Hochdeutsch.", "estimated_minutes": 45},
            {"id": "c2-06", "title": "Etymologie & Historische Grammatikentwicklung (Kelime K├Âkenleri)", "category": "Dilbilim", "description": "Almanca kelimelerin tarihsel k├Âkeni ve evrimi.", "estimated_minutes": 50},
            {"id": "c2-07", "title": "Nuancenreiche ├£bersetzungstheorie DE-TR / TR-DE (Akademik ├çeviri)", "category": "├çeviribilim", "description": "Metin t├╝r├╝ne g├Âre ├ğeviri stratejileri.", "estimated_minutes": 50},
            {"id": "c2-08", "title": "Diplomatische & Verhandlungssprache (├£st D├╝zey M├╝zakere Dili)", "category": "Diplomasi & ─░leti┼şim", "description": "Uluslararas─▒ ili┼şkiler ve m├╝zakere s├Âylemleri.", "estimated_minutes": 50}
        ]
    }
}
