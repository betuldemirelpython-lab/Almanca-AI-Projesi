
        let fullCatalogData = null;
        let currentActiveAnalysisData = null;
        let currentWritingAnalysisData = null;
        let currentStoryData = null;
        let isAudioPlaying = false;

        document.addEventListener('DOMContentLoaded', async () => {
            initTabs();
            initLevelChips();
            await fetchLevelsCatalog();
            initWritingCoach();
            initStoryModule();
            initAudioPlayer();
            initConjugator();
            initTranslator();
            initSummarizer();
            initPDFExport();
            initThemeToggle();
            initGrammarElement();
        });

        async function fetchLevelsCatalog() {
            try {
                const res = await fetch('/api/levels');
                const data = await res.json();
                fullCatalogData = data.catalog;
                renderLevelTopics('A1');
            } catch (e) {
                renderLevelTopics('A1');
            }
        }

        // Theme Toggle
        function initThemeToggle() {
            const btn = document.getElementById('themeToggleBtn');
            btn.addEventListener('click', () => {
                document.documentElement.classList.toggle('light-theme');
                const isLight = document.documentElement.classList.contains('light-theme');
                btn.innerHTML = isLight ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
            });
        }

        // Tab Navigation
        function initTabs() {
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => {
                btn.addEventListener('click', () => {
                    buttons.forEach(b => b.classList.remove('active'));
                    document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
                    
                    btn.classList.add('active');
                    const tabId = btn.getAttribute('data-tab');
                    document.getElementById(tabId).classList.add('active');
                });
            });
        }

        // Level Chips (A1-C2)
        function initLevelChips() {
            const chips = document.querySelectorAll('#levelsNavChips .level-chip');
            chips.forEach(chip => {
                chip.addEventListener('click', () => {
                    chips.forEach(c => c.classList.remove('active'));
                    chip.classList.add('active');
                    const level = chip.getAttribute('data-level');
                    renderLevelTopics(level);
                });
            });
        }

        function renderLevelTopics(level) {
            const container = document.getElementById('topicsGridContainer');
            container.innerHTML = '';
            
            let topics = [];
            if (fullCatalogData && fullCatalogData[level]) {
                topics = fullCatalogData[level].topics || [];
            }

            if (topics.length === 0) {
                container.innerHTML = `
                    <div class="topic-card" style="border-color: var(--accent-rose);">
                        <div>
                            <div class="topic-category" style="color: var(--accent-rose);">⚠️ BAĞLANTI HATASI</div>
                            <div class="topic-title">Konular Yüklenemedi</div>
                            <div class="topic-desc">Eğer bu dosyayı doğrudan tarayıcıda açtıysanız (file://), güvenlik nedeniyle arka plana bağlanamazsınız. Lütfen projeyi Vercel üzerinden veya yerel sunucudan (localhost:8000) çalıştırın.</div>
                        </div>
                    </div>
                `;
                return;
            }

            topics.forEach(t => {
                const card = document.createElement('div');
                card.className = 'topic-card';
                card.innerHTML = `
                    <div>
                        <div class="topic-category">${t.category}</div>
                        <div class="topic-title">${t.title}</div>
                        <div class="topic-desc">${t.description}</div>
                    </div>
                    <div class="topic-footer">
                        <span><i class="fa-regular fa-clock"></i> ${t.estimated_minutes || 20} dk</span>
                        <button class="btn-analyze-sm">Analiz Et <i class="fa-solid fa-chevron-right"></i></button>
                    </div>
                `;
                card.addEventListener('click', () => {
                    document.querySelector('[data-tab="tab-summarizer"]').click();
                    document.getElementById('customTopicInput').value = t.title;
                    document.getElementById('customLevelSelect').value = level;
                    triggerTopicAnalysis(t.title, level);
                });
                container.appendChild(card);
            });
        }

        // --- AI METİN ANALİZİ & YAZIM KOÇU (SKORLAMA & DÜZELTME) ---
        function initWritingCoach() {
            document.getElementById('btnEvaluateWriting').addEventListener('click', async () => {
                const text = document.getElementById('writingTextInput').value.trim();
                const targetLevel = document.getElementById('writingTargetLevelSelect').value;
                if (!text) return;

                showLoader("Metniniz dilbilgisi ve seviye yönünden değerlendiriliyor...");
                try {
                    const provider = document.getElementById('aiProviderSelect').value;
                    const res = await fetch('/api/evaluate-writing', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ text: text, target_level: targetLevel, provider: provider })
                    });
                    const data = await res.json();
                    renderWritingEvaluation(data);
                } catch (err) {
                    renderMockWritingEvaluation(text, targetLevel);
                } finally {
                    hideLoader();
                }
            });

            document.getElementById('btnExportWritingPDF').addEventListener('click', () => {
                if (!currentWritingAnalysisData) return;
                const md = `
# Almanca Metin Analiz & Skor Raporu (${currentWritingAnalysisData.target_level})
**Genel Puan:** ${currentWritingAnalysisData.overall_score} / 100
**Değerlendirilen Seviye:** ${currentWritingAnalysisData.assessed_level}

## Orjinal Metniniz
${currentWritingAnalysisData.original_text}

## Düzeltilmiş Mükemmel Metin
${currentWritingAnalysisData.corrected_text}

## Tespit Edilen Hatalar ve Açıklamaları
${(currentWritingAnalysisData.errors || []).map(e => `- **Hata:** ${e.original} ➔ **Doğru:** ${e.correction} (${e.error_type})\n  *Açıklama:* ${e.explanation_tr}`).join('\n\n')}
                `;
                downloadPDF(`Metin_Skor_${currentWritingAnalysisData.overall_score}`, md);
            });
        }

        function renderWritingEvaluation(data) {
            currentWritingAnalysisData = data;
            document.getElementById('writingAnalysisResult').style.display = 'block';
            
            // Score circle rendering
            const scoreNum = data.overall_score || 85;
            const scoreElem = document.getElementById('scoreCircleElem');
            document.getElementById('scoreNumberText').innerText = scoreNum;
            
            if (scoreNum >= 80) {
                scoreElem.className = "score-circle";
            } else if (scoreNum >= 60) {
                scoreElem.className = "score-circle medium-score";
            } else {
                scoreElem.className = "score-circle low-score";
            }

            document.getElementById('writingAssessedLevelText').innerText = data.assessed_level;
            document.getElementById('writingCorrectedText').innerText = data.corrected_text;

            // Error list
            const errArea = document.getElementById('writingErrorsList');
            errArea.innerHTML = '';
            (data.errors || []).forEach(e => {
                errArea.innerHTML += `
                    <div style="background: rgba(244, 63, 94, 0.08); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--accent-rose);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                            <span style="font-weight: 700; color: var(--accent-rose); font-size: 0.9rem;">❌ ${e.original}</span>
                            <span style="font-weight: 700; color: var(--accent-emerald); font-size: 0.9rem;">✅ ${e.correction}</span>
                        </div>
                        <p style="font-size: 0.8rem; color: var(--text-muted);"><b style="color: var(--accent-amber);">${e.error_type}:</b> ${e.explanation_tr}</p>
                    </div>
                `;
            });

            // Strengths & Improvements
            const sUl = document.getElementById('writingStrengthsList');
            sUl.innerHTML = '';
            (data.strengths || []).forEach(s => sUl.innerHTML += `<li>${s}</li>`);

            const iUl = document.getElementById('writingImprovementsList');
            iUl.innerHTML = '';
            (data.improvements || []).forEach(imp => iUl.innerHTML += `<li>${imp}</li>`);
        }

        function renderMockWritingEvaluation(text, level) {
            renderWritingEvaluation({
                original_text: text,
                target_level: level,
                overall_score: 88,
                assessed_level: `${level} - Başarılı Seviye`,
                corrected_text: text.replace("haben gegangen", "bin gegangen").replace("der Buch", "das Buch"),
                errors: [
                    {
                        original: "haben gegangen",
                        correction: "bin gegangen",
                        error_type: "Gramer (Yardımcı Fiil)",
                        explanation_tr: "Gehen fiili hareket/yer değiştirme bildirdiği için Perfekt geçmiş zamanda 'haben' yerine 'sein' (bin) kullanılır."
                    }
                ],
                strengths: [
                    "Cümle kurulumu ve kelime sırası doğru.",
                    "Seviyeye uygun bağlaçlar kullanılmış."
                ],
                improvements: [
                    "Artikel kullanımına (der/die/das) dikkat edilmeli.",
                    "Geçmiş zaman yardımcı fiil tercihleri gözden geçirilmeli."
                ]
            });
        }

        // --- İNTERAKTİF HİKAYE VE SES DİNLEME MODÜLÜ ---
        function initStoryModule() {
            document.getElementById('btnGenerateStory').addEventListener('click', async () => {
                const level = document.getElementById('storyLevelSelect').value;
                const theme = document.getElementById('storyThemeInput').value.trim() || "Günlük Yaşam";
                triggerStoryGeneration(level, theme);
            });

            document.getElementById('btnExportStoryPDF').addEventListener('click', () => {
                if (!currentStoryData) return;
                const md = `
# ${currentStoryData.title_de} (${currentStoryData.level})
*${currentStoryData.title_tr}*

## Hikaye Metni
${(currentStoryData.paragraphs || []).map(p => p.german_text).join('\n\n')}

## Türkçe Çeviri
${currentStoryData.full_translation_tr}
                `;
                downloadPDF(currentStoryData.title_de, md);
            });
        }

        function initAudioPlayer() {
            document.getElementById('btnPlayFullStory').addEventListener('click', () => {
                if (!currentStoryData) return;
                playFullStoryAudio();
            });

            document.getElementById('btnStopStoryAudio').addEventListener('click', () => {
                stopStoryAudio();
            });
        }

        function playFullStoryAudio() {
            if (!('speechSynthesis' in window)) {
                alert("Tarayıcınız sesli okuma özelliğini desteklemiyor.");
                return;
            }

            stopStoryAudio();

            const paragraphs = currentStoryData.paragraphs || [];
            if (paragraphs.length === 0) return;

            isAudioPlaying = true;
            let currentIdx = 0;

            const rate = parseFloat(document.getElementById('audioSpeedSelect').value) || 0.9;
            const pElements = document.querySelectorAll('#storyParagraphsArea .story-paragraph');

            function playNextParagraph() {
                if (!isAudioPlaying || currentIdx >= paragraphs.length) {
                    stopStoryAudio();
                    return;
                }

                pElements.forEach(p => p.classList.remove('audio-reading-active'));
                if (pElements[currentIdx]) {
                    pElements[currentIdx].classList.add('audio-reading-active');
                    pElements[currentIdx].scrollIntoView({ behavior: 'smooth', block: 'center' });
                }

                const textToRead = paragraphs[currentIdx].german_text;
                const utterance = new SpeechSynthesisUtterance(textToRead);
                utterance.lang = 'de-DE';
                utterance.rate = rate;

                utterance.onend = () => {
                    currentIdx++;
                    playNextParagraph();
                };

                utterance.onerror = () => {
                    stopStoryAudio();
                };

                window.speechSynthesis.speak(utterance);
            }

            playNextParagraph();
        }

        function stopStoryAudio() {
            isAudioPlaying = false;
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
            document.querySelectorAll('#storyParagraphsArea .story-paragraph').forEach(p => p.classList.remove('audio-reading-active'));
        }

        async function triggerStoryGeneration(level, theme) {
            stopStoryAudio();
            showLoader(`'${level}' seviyesinde '${theme}' konulu sesli hikaye üretiliyor...`);
            try {
                const provider = document.getElementById('aiProviderSelect').value;
                const res = await fetch('/api/generate-story', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ level: level, topic_theme: theme, provider: provider })
                });
                const data = await res.json();
                renderInteractiveStory(data);
            } catch (err) {
                renderMockInteractiveStory(level, theme);
            } finally {
                hideLoader();
            }
        }

        function renderInteractiveStory(data) {
            currentStoryData = data;
            document.getElementById('storyContainer').style.display = 'block';
            document.getElementById('storyLevelBadge').innerText = data.level;
            document.getElementById('storyTitleDE').innerText = data.title_de;
            document.getElementById('storyTitleTR').innerText = data.title_tr;
            document.getElementById('storyFullTransText').innerText = data.full_translation_tr;

            const area = document.getElementById('storyParagraphsArea');
            area.innerHTML = '';

            (data.paragraphs || []).forEach((para, idx) => {
                const pElem = document.createElement('div');
                pElem.className = 'story-paragraph';
                pElem.setAttribute('data-para-index', idx);

                (para.words || []).forEach(wordObj => {
                    const span = document.createElement('span');
                    span.className = 'hover-word';
                    span.innerText = wordObj.w + " ";
                    span.setAttribute('data-tr', wordObj.tr || 'Türkçe anlamı');
                    const subInfo = (wordObj.article ? `Artikel: ${wordObj.article} | ` : '') + (wordObj.type || '');
                    span.setAttribute('data-sub', subInfo);
                    
                    span.addEventListener('click', (e) => {
                        e.stopPropagation();
                        speakText(wordObj.w);
                    });

                    pElem.appendChild(span);
                });

                area.appendChild(pElem);
            });
        }

        function renderMockInteractiveStory(level, theme) {
            renderInteractiveStory({
                title_de: `Ein unvergesslicher Tag in Deutschland (${level})`,
                title_tr: `Almanya'da Unutulmaz Bir Gün (${level} Seviyesi - ${theme})`,
                level: level,
                paragraphs: [
                    {
                        german_text: "Heute steht Lukas früh am Morgen auf und öffnet das Fenster.",
                        words: [
                            { w: "Heute", tr: "Bugün", type: "Adverb" },
                            { w: "steht", tr: "kalkıyor (aufstehen)", type: "Verb" },
                            { w: "Lukas", tr: "Lukas", type: "Nomen" },
                            { w: "früh", tr: "erken", type: "Adjektiv" },
                            { w: "am", tr: "sabahleyin", type: "Präposition" },
                            { w: "Morgen", tr: "sabah", type: "Nomen", article: "der" },
                            { w: "auf", tr: "kalkmak (ayrılan ek)", type: "Verb-Präfix" },
                            { w: "und", tr: "ve", type: "Konnektor" },
                            { w: "öffnet", tr: "açıyor (öffnen)", type: "Verb" },
                            { w: "das", tr: "belirli artikel", type: "Artikel" },
                            { w: "Fenster.", tr: "pencere", type: "Nomen", article: "das" }
                        ]
                    },
                    {
                        german_text: "Die Sonne scheint hell und das Wetter ist wirklich wunderschön.",
                        words: [
                            { w: "Die", tr: "belirli artikel", type: "Artikel" },
                            { w: "Sonne", tr: "güneş", type: "Nomen", article: "die" },
                            { w: "scheint", tr: "parlıyor", type: "Verb" },
                            { w: "hell", tr: "parlak", type: "Adjektiv" },
                            { w: "und", tr: "ve", type: "Konnektor" },
                            { w: "das", tr: "belirli artikel", type: "Artikel" },
                            { w: "Wetter", tr: "hava", type: "Nomen", article: "das" },
                            { w: "ist", tr: "-dir", type: "Verb" },
                            { w: "wirklich", tr: "gerçekten", type: "Adverb" },
                            { w: "wunderschön.", tr: "harika", type: "Adjektiv" }
                        ]
                    },
                    {
                        german_text: "Lukas geht zuerst in die Bäckerei und kauft frische Brötchen.",
                        words: [
                            { w: "Lukas", tr: "Lukas", type: "Nomen" },
                            { w: "geht", tr: "gidiyor", type: "Verb" },
                            { w: "zuerst", tr: "öncelikle", type: "Adverb" },
                            { w: "in", tr: "-e, içine", type: "Präposition" },
                ],
                full_translation_tr: "Bugün Lukas süpermarkete gidiyor. Taze ekmek ve taze süt satın alıyor."
            });
        }

        // Web Speech API Pronunciation
        function speakText(text, lang = 'de-DE') {
            if (!text || !text.trim()) return;
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = lang;
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }
        }

        function speakInputText() {
            const txt = document.getElementById('transInput').value.trim();
            if (!txt) return;
            const dir = document.getElementById('transDirection').value;
            const lang = dir === 'de-tr' ? 'de-DE' : 'tr-TR';
            speakText(txt, lang);
        }

        function speakOutputText() {
            const txt = document.getElementById('mainTranslationText').innerText.trim();
            if (!txt || txt === 'Çeviri sonucu burada görünecek...') return;
            const dir = document.getElementById('transDirection').value;
            const lang = dir === 'de-tr' ? 'tr-TR' : 'de-DE';
            speakText(txt, lang);
        }

        // --- FİİL ÇEKİM MATRİSİ ---
        function initConjugator() {
            document.getElementById('conjugationForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const verb = document.getElementById('verbInput').value.trim();
                if (!verb) return;

                showLoader(`'${verb}' fiili tüm zamanlara çekimleniyor...`);
                try {
                    const provider = document.getElementById('aiProviderSelect').value;
                    const res = await fetch('/api/conjugate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ verb: verb, provider: provider })
                    });
                    const data = await res.json();
                    renderConjugation(data);
                } catch (err) {
                    renderMockConjugation(verb);
                } finally {
                    hideLoader();
                }
            });
        }

        function renderConjugation(data) {
            document.getElementById('verbMetaBanner').style.display = 'block';
            document.getElementById('metaVerbTitle').innerText = data.verb;
            document.getElementById('metaMeaning').innerText = `Türkçe: ${data.turkish_meaning}`;
            
            const auxSpan = document.getElementById('metaAux');
            auxSpan.innerText = `Yardımcı: ${data.auxiliary_verb}`;
            auxSpan.className = data.auxiliary_verb === 'sein' ? 'article-badge article-das' : 'article-badge article-der';

            const regSpan = document.getElementById('metaRegular');
            regSpan.innerText = data.is_regular ? "Düzenli Fiil" : "Düzensiz Fiil";
            regSpan.className = data.is_regular ? 'article-badge article-das' : 'article-badge article-die';

            document.getElementById('metaStamm').innerText = data.stammformen || '';

            const grid = document.getElementById('verbMatrixGrid');
            grid.innerHTML = '';

            (data.tenses || []).forEach(t => {
                const card = document.createElement('div');
                card.className = 'tense-card';
                card.innerHTML = `
                    <div class="tense-header">
                        <span class="tense-title">${t.tense_name}</span>
                        <span class="tense-sub">${t.turkish_tense_name}</span>
                    </div>
                    <div class="pronoun-list">
                        ${Object.entries(t.forms || {}).map(([p, f]) => `
                            <div class="pronoun-row">
                                <span class="pronoun-tag">${p.replace('_sie_es', '/sie/es').replace('_Sie', '/Sie')}</span>
                                <span class="conjugated-form">${f}</span>
                                <button onclick="speakText('${f}')" class="audio-btn"><i class="fa-solid fa-volume-high"></i></button>
                            </div>
                        `).join('')}
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function renderMockConjugation(verb) {
            // Gehen örneğini özel olarak düzelt, diğerleri için uyarı ver
            if (verb.toLowerCase() === "gehen") {
                renderConjugation({
                    verb: "gehen",
                    turkish_meaning: "gitmek (Demo API Key Uyarısı)",
                    is_regular: false,
                    auxiliary_verb: "sein",
                    stammformen: "gehen - ging - ist gegangen",
                    tenses: [
                        {
                            tense_name: "Präsens",
                            turkish_tense_name: "Şimdiki / Geniş Zaman",
                            forms: { "ich": "ich gehe", "du": "du gehst", "er_sie_es": "er/sie/es geht", "wir": "wir gehen", "ihr": "ihr geht", "sie_Sie": "sie/Sie gehen" }
                        }
                    ]
                });
            } else {
                renderConjugation({
                    verb: verb,
                    turkish_meaning: `(API Key Gerekli) ${verb} fiili`,
                    is_regular: true,
                    auxiliary_verb: "haben/sein",
                    stammformen: `Lütfen .env veya Vercel'e API Key girin.`,
                    tenses: [
                        {
                            tense_name: "⚠️ HATA",
                            turkish_tense_name: "Demo Modu",
                            forms: { "ich": `API Key Eksik`, "du": `API Key Eksik`, "er_sie_es": `API Key Eksik`, "wir": `API Key Eksik`, "ihr": `API Key Eksik`, "sie_Sie": `API Key Eksik` }
                        }
                    ]
                });
            }
        }

        // Translator
        function initTranslator() {
            document.getElementById('btnTranslate').addEventListener('click', async () => {
                const text = document.getElementById('transInput').value.trim();
                if (!text) return;
                showLoader("Kelime & Dilbilgisi Çevirisi Yapılıyor...");
                try {
                    const provider = document.getElementById('aiProviderSelect').value;
                    const dir = document.getElementById('transDirection').value;
                    const res = await fetch('/api/translate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ text: text, direction: dir, provider: provider })
                    });
                    const data = await res.json();
                    renderDictCard(data);
                } catch (err) {
                    renderDictCard({
                        source_text: text,
                        main_translation: `⚠️ API Key Eksik (Demo Çeviri): ${text}`,
                        dictionary_entry: {
                            german: text,
                            turkish: `Lütfen gerçek çeviri için .env veya Vercel'den API Key girin.`,
                            article: "das",
                            plural: "die Wörter",
                            phonetic: "[vɔrt]",
                            examples: [{ german: `API Key bulunamadı.`, turkish: `Sistem demo modunda çalışıyor.` }]
                        }
                    });
                } finally {
                    hideLoader();
                }
            });
        }

        function renderDictCard(data) {
            document.getElementById('dictContentEmpty').style.display = 'none';
            document.getElementById('dictContentActive').style.display = 'block';

            const mainTransText = document.getElementById('mainTranslationText');
            if (data.main_translation) {
                mainTransText.innerText = data.main_translation;
            } else {
                mainTransText.innerText = 'Çeviri bulunamadı.';
            }

            const entry = data.dictionary_entry || {};
            const artBadge = document.getElementById('dictArticleBadge');
            if (entry.article) {
                artBadge.style.display = 'inline-block';
                artBadge.innerText = entry.article;
                artBadge.className = `article-badge article-${entry.article}`;
            } else {
                artBadge.style.display = 'none';
            }

            document.getElementById('dictGermanWord').innerText = entry.german || data.source_text;
            document.getElementById('dictPhonetic').innerText = entry.phonetic || '';
            document.getElementById('dictTurkishWord').innerText = `Türkçe: ${entry.turkish || 'Belirtilmedi'}`;
            document.getElementById('dictPlural').innerHTML = `<b>Çoğul:</b> ${entry.plural || 'Belirtilmedi'}`;

            const exList = document.getElementById('dictExamplesList');
            exList.innerHTML = '';
            (entry.examples || []).forEach(ex => {
                const safeDe = (ex.german || '').replace(/'/g, "\\'");
                exList.innerHTML += `
                    <div style="background: rgba(255,255,255,0.03); padding: 0.6rem 0.85rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; gap: 0.5rem;">
                        <div>
                            <p style="font-weight: 600; margin: 0; font-size: 0.95rem;">${ex.german}</p>
                            <p style="color: var(--text-muted); font-size: 0.8rem; margin: 0.2rem 0 0;">${ex.turkish}</p>
                        </div>
                        <button onclick="speakText('${safeDe}')" class="audio-btn" style="flex-shrink: 0;" title="Cümleyi Dinle">
                            <i class="fa-solid fa-volume-high"></i>
                        </button>
                    </div>
                `;
            });
        }

        // Summarizer & Analysis
        function initSummarizer() {
            document.getElementById('btnAnalyzeTopic').addEventListener('click', () => {
                const topic = document.getElementById('customTopicInput').value.trim();
                const level = document.getElementById('customLevelSelect').value;
                if (topic) triggerTopicAnalysis(topic, level);
            });
        }

        async function triggerTopicAnalysis(topic, level) {
            showLoader(`'${topic}' konusu detaylı analiz ediliyor...`);
            try {
                const provider = document.getElementById('aiProviderSelect').value;
                const res = await fetch('/api/analyze-topic', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ topic: topic, level: level, provider: provider })
                });
                const data = await res.json();
                renderTopicAnalysis(data);
            } catch (err) {
                renderMockTopicAnalysis(topic, level);
            } finally {
                hideLoader();
            }
        }

        function renderTopicAnalysis(data) {
            currentActiveAnalysisData = data;
            document.getElementById('topicAnalysisResult').style.display = 'block';
            document.getElementById('analysisTitle').innerText = `${data.level} - ${data.topic}`;

            // Formula Structure
            const formulaBox = document.getElementById('analysisFormulaBox');
            const formulaText = document.getElementById('analysisFormulaText');
            if (data.formula_structure) {
                formulaBox.style.display = 'block';
                formulaText.innerText = data.formula_structure;
            } else {
                formulaBox.style.display = 'none';
            }

            // Multi-paragraph Summary
            const summaryDiv = document.getElementById('analysisSummaryText');
            summaryDiv.innerHTML = (data.summary_tr || '')
                .split('\n\n')
                .map(p => `<p style="margin-bottom: 0.8rem;">${p.replace(/\n/g, '<br>')}</p>`)
                .join('');

            // Key Grammar Rules
            const rulesUl = document.getElementById('analysisRulesList');
            rulesUl.innerHTML = '';
            (data.key_grammar_rules || []).forEach(r => {
                rulesUl.innerHTML += `<li style="margin-bottom: 0.4rem;">${r}</li>`;
            });

            // Usage Notes
            const notesUl = document.getElementById('analysisNotesList');
            notesUl.innerHTML = '';
            (data.usage_notes || []).forEach(n => {
                notesUl.innerHTML += `<li style="margin-bottom: 0.4rem;">${n}</li>`;
            });

            // Vocabulary Grid
            const vocabSec = document.getElementById('analysisVocabSection');
            const vocabGrid = document.getElementById('analysisVocabGrid');
            if (data.vocabulary && data.vocabulary.length > 0) {
                vocabSec.style.display = 'block';
                vocabGrid.innerHTML = '';
                data.vocabulary.forEach(v => {
                    const artClass = v.article ? `article-${v.article.toLowerCase()}` : '';
                    const safeGerm = (v.german || '').replace(/'/g, "\\'");
                    vocabGrid.innerHTML += `
                        <div style="background: rgba(255,255,255,0.03); padding: 0.75rem; border-radius: 10px; border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                            <div>
                                ${v.article ? `<span class="article-badge ${artClass}">${v.article}</span>` : ''}
                                <span style="font-weight: 700; font-size: 0.95rem;">${v.german}</span>
                                <span onclick="speakText('${safeGerm}')" class="audio-btn" style="cursor: pointer; margin-left: 0.3rem;" title="Dinle"><i class="fa-solid fa-volume-high"></i></span>
                                <div style="font-size: 0.8rem; color: var(--accent-emerald); margin-top: 0.2rem;">${v.turkish}</div>
                                ${v.plural ? `<div style="font-size: 0.75rem; color: var(--text-muted);">Çoğul: ${v.plural}</div>` : ''}
                            </div>
                        </div>
                    `;
                });
            } else {
                vocabSec.style.display = 'none';
            }

            // Sentence Examples with Audio
            const examplesList = document.getElementById('analysisExamplesList');
            if (examplesList) {
                examplesList.innerHTML = '';
                (data.examples || []).forEach(ex => {
                    const safeDe = (ex.german || '').replace(/'/g, "\\'");
                    examplesList.innerHTML += `
                        <div style="background: rgba(255,255,255,0.03); padding: 0.85rem 1rem; border-radius: 10px; border-left: 4px solid var(--accent-primary); display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
                            <div>
                                <div style="font-weight: 700; font-size: 1.05rem; color: var(--text-main);">${ex.german}</div>
                                <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem;">${ex.turkish}</div>
                            </div>
                            <button onclick="speakText('${safeDe}')" class="btn-audio-control" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;" title="Dinle">
                                <i class="fa-solid fa-volume-high"></i> Dinle
                            </button>
                        </div>
                    `;
                });
            }

            // Common Mistakes
            const mistakesUl = document.getElementById('analysisMistakesList');
            mistakesUl.innerHTML = '';
            (data.common_mistakes || []).forEach(m => {
                mistakesUl.innerHTML += `<li style="margin-bottom: 0.5rem; background: rgba(244,63,94,0.05); padding: 0.6rem; border-radius: 8px;">${m}</li>`;
            });

            // Mini Quiz Area
            const quizArea = document.getElementById('analysisQuizArea');
            quizArea.innerHTML = '';
            if (data.mini_quiz && data.mini_quiz.length > 0) {
                data.mini_quiz.forEach((q, qIdx) => {
                    const qBox = document.createElement('div');
                    qBox.style.cssText = 'background: rgba(255,255,255,0.02); padding: 1.25rem; border-radius: 10px; border: 1px solid var(--border-color);';
                    
                    let optionsHTML = '';
                    (q.options || []).forEach((opt) => {
                        const safeOpt = opt.replace(/"/g, '&quot;');
                        optionsHTML += `
                            <button class="quiz-option-btn" data-qindex="${qIdx}" data-opt="${safeOpt}" style="text-align: left; background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-main); padding: 0.6rem 1rem; border-radius: 8px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s ease;">
                                ${opt}
                            </button>
                        `;
                    });

                    qBox.innerHTML = `
                        <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.8rem; color: var(--text-main);">
                            <span style="color: var(--accent-emerald);">Soru ${qIdx + 1}:</span> ${q.question}
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 0.8rem;">
                            ${optionsHTML}
                        </div>
                        <div id="quizExp_${qIdx}" style="display: none; padding: 0.75rem; border-radius: 8px; font-size: 0.85rem; line-height: 1.5;"></div>
                    `;
                    quizArea.appendChild(qBox);
                });

                // Attach Quiz Option Event Listeners
                quizArea.querySelectorAll('.quiz-option-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const qIdx = parseInt(btn.getAttribute('data-qindex'));
                        const selectedOpt = btn.getAttribute('data-opt');
                        const quizData = data.mini_quiz[qIdx];
                        const expDiv = document.getElementById(`quizExp_${qIdx}`);
                        
                        const isCorrect = selectedOpt.trim().startsWith(quizData.correct_answer.trim().substring(0, 2)) || 
                                          selectedOpt.trim() === quizData.correct_answer.trim();

                        if (isCorrect) {
                            btn.style.background = 'rgba(16, 185, 129, 0.2)';
                            btn.style.borderColor = 'var(--accent-emerald)';
                            btn.style.color = 'var(--accent-emerald)';
                            expDiv.style.display = 'block';
                            expDiv.style.background = 'rgba(16, 185, 129, 0.1)';
                            expDiv.style.border = '1px solid var(--accent-emerald)';
                            expDiv.style.color = 'var(--accent-emerald)';
                            expDiv.innerHTML = `<b>✅ Doğru Cevap!</b> ${quizData.explanation || ''}`;
                        } else {
                            btn.style.background = 'rgba(244, 63, 94, 0.2)';
                            btn.style.borderColor = 'var(--accent-rose)';
                            btn.style.color = 'var(--accent-rose)';
                            expDiv.style.display = 'block';
                            expDiv.style.background = 'rgba(244, 63, 94, 0.1)';
                            expDiv.style.border = '1px solid var(--accent-rose)';
                            expDiv.style.color = 'var(--accent-rose)';
                            expDiv.innerHTML = `<b>❌ Yanlış Cevap.</b> Doğru Şık: <b>${quizData.correct_answer}</b><br>${quizData.explanation || ''}`;
                        }
                    });
                });
            } else {
                quizArea.innerHTML = `<p style="color: var(--text-muted); font-size: 0.85rem;">Bu konu için henüz quiz sorusu üretilmedi.</p>`;
            }
        }

        function renderMockTopicAnalysis(topic, level) {
            renderTopicAnalysis({
                topic: topic,
                level: level,
                summary_tr: `'${topic}' konusu (${level} seviyesi), Almancanın temel yapı taşlarından biridir. Bu konuda isim çekimleri, fiil pozisyonları ve artikel kuralları büyük önem taşır.\n\nSistem şu an demo modunda çalışmaktadır. Yapay zeka ile tam analiz için lütfen Vercel veya .env dosyasından API anahtarınızı girin.`,
                formula_structure: "[Özne] + [Fiil (2. Sıra)] + [Nesne] + ... + [İkinci Fiil (Sonda)]",
                key_grammar_rules: [
                    "Ana cümlelerde fiil 2. pozisyondadır.",
                    "Artikeller ismin haline (Nominativ, Akkusativ, Dativ) göre değişir.",
                    "Modal fiil cümlenin 2. sırasındayken esas fiil mastar (Infinitiv) halde en sona gider."
                ],
                usage_notes: [
                    "İpucu: Almanca öğrenirken isimleri mutlaka artikelleriyle ezberleyin.",
                    "Türkçeden farklı olarak fiil ana cümlede en sonda değil, 2. sıradadır."
                ],
                vocabulary: [
                    { german: "das Buch", turkish: "kitap", article: "das", plural: "die Bücher" },
                    { german: "die Sprache", turkish: "dil", article: "die", plural: "die Sprachen" }
                ],
                examples: [
                    { german: "Ich lerne jeden Tag Deutsch.", turkish: "Her gün Almanca öğreniyorum." },
                    { german: "Wir trinken heute Kaffee.", turkish: "Bugün kahve içiyoruz." }
                ],
                common_mistakes: [
                    "Yanlış: Ich nach Hause gehe. -> Doğru: Ich gehe nach Hause."
                ],
                mini_quiz: [
                    {
                        question: "Almanca düz ana cümlede fiil kaçıncı sırada yer almalıdır?",
                        options: ["A) 1. sırada", "B) 2. sırada", "C) En sonda"],
                        correct_answer: "B) 2. sırada",
                        explanation: "Almanca ana cümlelerde fiil her zaman 2. pozisyondadır."
                    }
                ]
            });
        }

        // PDF Export
        function initPDFExport() {
            document.getElementById('btnExportPDFCurrent').addEventListener('click', () => {
                if (!currentActiveAnalysisData) return;
                const md = `
# ${currentActiveAnalysisData.level} - ${currentActiveAnalysisData.topic}

## Konu Özeti
${currentActiveAnalysisData.summary_tr}

## Temel Gramer Kuralları
${(currentActiveAnalysisData.key_grammar_rules || []).map(r => '- ' + r).join('\n')}

## Sık Yapılan Hatalar
${(currentActiveAnalysisData.common_mistakes || []).map(m => '- ' + m).join('\n')}
                `;
                downloadPDF(currentActiveAnalysisData.topic, md);
            });

            document.getElementById('btnGeneratePDFCustom').addEventListener('click', () => {
                const title = document.getElementById('pdfReportTitle').value.trim() || "Almanca Çalışma Raporu";
                const content = document.getElementById('pdfReportContent').value.trim();
                if (content) downloadPDF(title, content);
            });
        }

        async function downloadPDF(title, markdownContent) {
            try {
                const res = await fetch('/api/export-pdf', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        title: title,
                        content_markdown: markdownContent,
                        author: "Betül Altınkaynak Demirel"
                    })
                });
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Almanca_Rapor_${title.replace(/\s+/g, '_')}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
            } catch (err) {
                alert("PDF indirilemedi.");
            }
        }

        // Helpers
        function showLoader(txt) {
            document.getElementById('loaderText').innerText = txt || 'Yapay Zeka Analiz Yapıyor...';
            document.getElementById('appLoader').style.display = 'block';
        }

        function hideLoader() {
            document.getElementById('appLoader').style.display = 'none';
        }

        // *** Edat / Zamir / Bağlaç / Sıfat Analiz Modülü ***
        function fillGrammarElement(element, category) {
            document.getElementById('grammarElementInput').value = element;
            const sel = document.getElementById('grammarCategorySelect');
            for (let i = 0; i < sel.options.length; i++) {
                if (sel.options[i].value === category) { sel.selectedIndex = i; break; }
            }
            document.querySelector('[data-tab="tab-grammar-element"]').click();
            document.getElementById('btnAnalyzeGrammarElement').click();
        }

        function initGrammarElement() {
            const btn = document.getElementById('btnAnalyzeGrammarElement');
            btn.addEventListener('click', async () => {
                const element = document.getElementById('grammarElementInput').value.trim();
                const category = document.getElementById('grammarCategorySelect').value;
                if (!element) {
                    alert('Lütfen analiz edilecek yapıyı veya kelimeyi girin (örn: je...desto, weil, mit).');
                    return;
                }
                showLoader(`"${element}" yapısı analiz ediliyor...`);
                try {
                    const res = await fetch('/api/grammar-element', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ element, category, provider: 'gemini' })
                    });
                    if (!res.ok) throw new Error(`HTTP ${res.status}`);
                    const data = await res.json();
                    renderGrammarElementResult(data);
                } catch (err) {
                    document.getElementById('grammarElementResult').style.display = 'block';
                    document.getElementById('grammarElementResult').innerHTML = `
                        <div class="ge-card" style="border-color: var(--accent-rose);">
                            <h3 style="color: var(--accent-rose);"><i class="fa-solid fa-circle-exclamation"></i> Hata</h3>
                            <p>${err.message}</p>
                        </div>`;
                } finally {
                    hideLoader();
                }
            });
        }

        function renderGrammarElementResult(d) {
            const categoryIcons = { 'Bağlaç': '🔗', 'Edat': '📍', 'Zamir': '👤', 'Sıfat': '🎨' };
            const icon = categoryIcons[d.category] || '📚';

            // Examples table rows
            const exampleRows = (d.examples || []).map(ex => `
                <tr>
                    <td>${escapeHtml(ex.german)}</td>
                    <td style="color: var(--text-muted);">${escapeHtml(ex.turkish)}</td>
                </tr>`).join('');

            // Rules list
            const ruleItems = (d.rules || []).map(r => `<li>${escapeHtml(r)}</li>`).join('');

            // Tips list
            const tipItems = (d.tips || []).map(t => `<li>${escapeHtml(t)}</li>`).join('');

            // Mistakes list
            const mistakeItems = (d.common_mistakes || []).map(m => `<li>${escapeHtml(m)}</li>`).join('');

            // Quiz cards
            const quizCards = (d.quiz || []).map((q, qi) => {
                const opts = (q.options || []).map((opt, oi) => `
                    <button class="ge-quiz-option" onclick="checkGrammarQuiz(this, '${escapeAttr(opt)}', '${escapeAttr(q.correct_answer)}', 'ge-quiz-exp-${qi}')">
                        ${escapeHtml(opt)}
                    </button>`).join('');
                return `
                    <div class="ge-quiz-card">
                        <p style="font-weight: 700; margin-bottom: 0.75rem; font-size: 0.95rem;">${qi+1}. ${escapeHtml(q.question)}</p>
                        ${opts}
                        <p id="ge-quiz-exp-${qi}" style="display:none; margin-top:0.75rem; font-size:0.85rem; color:var(--accent-emerald); font-weight:600;">
                            ✅ ${escapeHtml(q.explanation || '')}
                        </p>
                    </div>`;
            }).join('');

            const html = `
                <!-- Header -->
                <div class="ge-card" style="background: linear-gradient(135deg, rgba(59,130,246,0.07), rgba(139,92,246,0.07)); border-color: rgba(139,92,246,0.3);">
                    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.75rem;">
                        <div>
                            <h2 style="font-size:1.6rem; font-weight:800; font-family:'Outfit',sans-serif; margin-bottom:0.3rem;">
                                ${icon} <span style="color:var(--accent-secondary);">${escapeHtml(d.element)}</span>
                            </h2>
                            <div>
                                <span class="ge-badge">${escapeHtml(d.category)}</span>
                                <span class="ge-badge" style="background:linear-gradient(135deg,var(--accent-emerald),#059669);">${escapeHtml(d.level || '')}</span>
                                <span style="font-size:0.85rem; color:var(--text-muted);">${escapeHtml(d.german_type || '')}</span>
                            </div>
                        </div>
                        <div style="background:var(--bg-primary); border-radius:10px; padding:0.75rem 1.25rem; border:1px solid var(--border-color); max-width:320px;">
                            <p style="font-size:0.75rem; color:var(--text-muted); font-weight:700; margin-bottom:0.2rem;">TÜRKÇE KARŞILIĞI</p>
                            <p style="font-size:1rem; font-weight:700; color:var(--accent-amber);">${escapeHtml(d.turkish_meaning || '')}</p>
                        </div>
                    </div>
                </div>

                ${d.formula ? `
                <!-- Formula -->
                <div class="ge-card">
                    <h3><i class="fa-solid fa-code" style="color:var(--accent-secondary);"></i> Cümle Yapısı / Formülü</h3>
                    <div class="ge-formula">${escapeHtml(d.formula)}</div>
                </div>` : ''}

                <!-- Explanation -->
                <div class="ge-card">
                    <h3><i class="fa-solid fa-book-open" style="color:var(--accent-primary);"></i> Açıklama</h3>
                    <p style="line-height:1.8; font-size:0.95rem; color:var(--text-muted);">${escapeHtml(d.explanation_tr || '')}</p>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                    <!-- Rules -->
                    <div class="ge-card">
                        <h3><i class="fa-solid fa-scale-balanced" style="color:var(--accent-primary);"></i> Dilbilgisi Kuralları</h3>
                        <ul class="ge-rule-list" style="list-style:none; padding:0;">${ruleItems}</ul>
                    </div>
                    <!-- Tips -->
                    <div class="ge-card">
                        <h3><i class="fa-solid fa-lightbulb" style="color:var(--accent-emerald);"></i> Püf Noktaları</h3>
                        <ul class="ge-tip-list" style="list-style:none; padding:0;">${tipItems || '<li>Genel kural olarak yapıyı cümle içinde uygulayın.</li>'}</ul>
                    </div>
                </div>

                <!-- Examples -->
                ${exampleRows ? `
                <div class="ge-card">
                    <h3><i class="fa-solid fa-list-check" style="color:var(--accent-amber);"></i> Örnek Cümleler</h3>
                    <table class="ge-example-table">
                        <thead>
                            <tr style="font-size:0.78rem; color:var(--text-muted); font-weight:700;">
                                <td style="padding-bottom:0.5rem;">🇩🇪 Almanca</td>
                                <td style="padding-bottom:0.5rem;">🇹🇷 Türkçe</td>
                            </tr>
                        </thead>
                        <tbody>${exampleRows}</tbody>
                    </table>
                </div>` : ''}

                <!-- Common Mistakes -->
                ${mistakeItems ? `
                <div class="ge-card">
                    <h3><i class="fa-solid fa-triangle-exclamation" style="color:var(--accent-rose);"></i> Sık Yapılan Hatalar</h3>
                    <ul class="ge-mistake-list" style="list-style:none; padding:0;">${mistakeItems}</ul>
                </div>` : ''}

                <!-- Quiz -->
                ${quizCards ? `
                <div class="ge-card">
                    <h3><i class="fa-solid fa-circle-question" style="color:var(--accent-amber);"></i> Mini Test</h3>
                    ${quizCards}
                </div>` : ''}
            `;

            const resultDiv = document.getElementById('grammarElementResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = html;
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function checkGrammarQuiz(btn, selected, correct, expId) {
            const container = btn.parentElement;
            const allOpts = container.querySelectorAll('.ge-quiz-option');
            allOpts.forEach(o => {
                o.disabled = true;
                if (o.innerText.trim() === correct.trim()) o.classList.add('correct');
                else o.classList.add('wrong');
            });
            const exp = document.getElementById(expId);
            if (exp) exp.style.display = 'block';
        }

        function escapeHtml(str) {
            if (!str) return '';
            return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
        }
        function escapeAttr(str) {
            if (!str) return '';
            return String(str).replace(/'/g,"\\'");
        }
    