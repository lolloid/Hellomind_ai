document.addEventListener("DOMContentLoaded", () => {
<<<<<<< HEAD
  /* =====================
     AUTH CHECK
  ===================== */
  const token = localStorage.getItem("hm_token");
  let userData = {};
  try {
    const rawUser = localStorage.getItem("hm_user");
    if (rawUser && rawUser !== "undefined") {
      userData = JSON.parse(rawUser);
    }
  } catch (e) {
    console.error("Failed to parse user data", e);
  }
  
  if (!token) {
    window.location.href = "/login";
    return;
  }

  // Set user info
  document.getElementById("userName").textContent = userData.username || "User";
  document.getElementById("userAvatar").textContent = (userData.username || "U").charAt(0).toUpperCase();

  window.logout = function() {
    localStorage.removeItem("hm_token");
    localStorage.removeItem("hm_user");
    window.location.href = "/login";
  };

  /* =====================
     I18N (MULTI-LANGUAGE)
  ===================== */
  const I18N = {
    id: {
      new_chat: "Obrolan Baru",
      history: "Riwayat",
      logout: "Keluar",
      hero_title: "HelloMind",
      hero_subtitle: "Tempat aman untuk ngobrol dan berbagi cerita.<br/>Tanpa dihakimi, tanpa dinilai.",
      prompt_1: "Aku lagi capek banget",
      prompt_2: "Lagi bingung soal hidup",
      prompt_3: "Aku ngerasa sendirian",
      prompt_4: "Aku butuh teman cerita",
      input_placeholder: "Ketik atau bicara pesanmu...",
      listening: "Mendengarkan...",
      disclaimer: "HelloMind bukan pengganti konsultasi profesional. Darurat: <strong>119 ext. 8</strong>",
      new_chat_title: "Obrolan Baru",
      rename_prompt: "Ubah nama obrolan:",
      delete_confirm: "Hapus obrolan ini?",
      default_reply: "Hmm, coba ulangi ya.",
      error_reply: "Maaf, lagi ada gangguan teknis. Coba lagi sebentar ya.",
      settings: "Pengaturan",
      settings_title: "Pengaturan Personalize",
      ai_name_label: "Nama AI",
      ai_persona_label: "Sifat & Persona AI",
      camera_privacy_title: "Aktifkan Kamera?",
      camera_privacy_body: "Kamera hanya dipakai di browser kamu untuk membaca ekspresi secara kasar agar obrolan terasa lebih peka. Video tidak disimpan dan tidak dikirim ke server.",
      camera_privacy_point_1: "Kamu bisa mematikannya kapan saja.",
      camera_privacy_point_2: "Hasil emosi hanya sinyal bantu, bukan penilaian pasti.",
      camera_allow: "Aktifkan",
      voice_ready: "Pesan suara siap dikirim",
      voice_error: "Mikrofon bermasalah. Coba lagi ya.",
      voice_clear: "Ulangi",
      voice_send: "Kirim",
      cancel: "Batal",
      save: "Simpan"
    },
    en: {
      new_chat: "New Chat",
      history: "History",
      logout: "Log Out",
      hero_title: "HelloMind",
      hero_subtitle: "A safe space to chat and share your feelings.<br/>No judgment, no grades.",
      prompt_1: "I'm feeling really exhausted",
      prompt_2: "I'm confused about life right now",
      prompt_3: "I feel so alone",
      prompt_4: "I need someone to talk to",
      input_placeholder: "Type or speak your message...",
      listening: "Listening...",
      disclaimer: "HelloMind is not a substitute for professional help. Emergency: <strong>911</strong>",
      new_chat_title: "New Chat",
      rename_prompt: "Rename chat:",
      delete_confirm: "Delete this chat?",
      default_reply: "Hmm, could you say that again?",
      error_reply: "Sorry, there's a technical issue. Please try again in a moment.",
      settings: "Settings",
      settings_title: "Personalization Settings",
      ai_name_label: "AI Name",
      ai_persona_label: "AI Traits & Persona",
      camera_privacy_title: "Enable Camera?",
      camera_privacy_body: "The camera is used only in your browser to roughly read expression cues so the chat can feel more emotionally aware. Video is not saved or sent to the server.",
      camera_privacy_point_1: "You can turn it off anytime.",
      camera_privacy_point_2: "Emotion results are only helpful cues, not definite judgments.",
      camera_allow: "Enable",
      voice_ready: "Voice message ready to send",
      voice_error: "Microphone had trouble. Please try again.",
      voice_clear: "Retry",
      voice_send: "Send",
      cancel: "Cancel",
      save: "Save"
    }
  };

  let currentLang = userData.language || "id";
  let recognition = null;

  function applyI18n() {
    const dict = I18N[currentLang];
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (dict[key]) el.innerHTML = dict[key];
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const key = el.getAttribute("data-i18n-placeholder");
      if (dict[key]) el.setAttribute("placeholder", dict[key]);
    });
    
    // Update language buttons
    document.getElementById("langId").classList.toggle("active", currentLang === "id");
    document.getElementById("langEn").classList.toggle("active", currentLang === "en");
    
    // Update speech recognition lang if active
    if (recognition) {
      recognition.lang = currentLang === "en" ? "en-US" : "id-ID";
    }
  }

  window.setLanguage = async function(lang) {
    if (lang === currentLang) return;
    currentLang = lang;
    userData.language = lang;
    localStorage.setItem("hm_user", JSON.stringify(userData));
    applyI18n();
    
    try {
      await fetch("/auth/settings", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ language: lang })
      });
    } catch(e) { console.error(e); }
  };

  window.getI18n = function(key) {
    return I18N[currentLang][key] || key;
  };

  applyI18n();

  /* =====================
     DOM ELEMENTS
  ===================== */
=======
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
  const chat = document.getElementById("chat");
  const input = document.getElementById("input");
  const sendBtn = document.getElementById("sendBtn");
  const newChatBtn = document.getElementById("newChatBtn");
  const hero = document.getElementById("hero");
  const historyDiv = document.getElementById("history");
<<<<<<< HEAD
  const cameraBtn = document.getElementById("cameraBtn");
  const webcamVideo = document.getElementById("webcamVideo");
  const webcamContainer = document.getElementById("webcamContainer");
  const webcamClose = document.getElementById("webcamClose");
  const emotionBadge = document.getElementById("emotionBadge");
  const emotionIcon = document.getElementById("emotionIcon");
  const emotionText = document.getElementById("emotionText");
  const textEmotionBadge = document.getElementById("textEmotionBadge");
  const textEmotionIcon = document.getElementById("textEmotionIcon");
  const textEmotionText = document.getElementById("textEmotionText");

  /* =====================
     STATE
  ===================== */
  let chats = [];
  let activeChat = null;
  let isSending = false;
  
  /* =====================
     API UTILS
  ===================== */
  async function apiFetch(url, options = {}) {
    options.headers = options.headers || {};
    options.headers["Authorization"] = `Bearer ${token}`;
    if (!options.headers["Content-Type"] && options.body && typeof options.body === 'string') {
        options.headers["Content-Type"] = "application/json";
    }
    
    const res = await fetch(url, options);
    if (res.status === 401) window.logout();
    if (!res.ok) throw new Error(`API Error: ${res.status}`);
    return res.json();
  }

  /* =====================
     TEXT-TO-SPEECH (TTS)
  ===================== */
  let ttsEnabled = false;
  const ttsBtn = document.getElementById("ttsBtn");
  const ttsIconOn = document.querySelector(".tts-icon-on");
  const ttsIconOff = document.querySelector(".tts-icon-off");
  let synthesis = window.speechSynthesis;

  if (ttsBtn) {
    ttsBtn.addEventListener("click", () => {
      ttsEnabled = !ttsEnabled;
      if (ttsEnabled) {
        ttsBtn.classList.add("active");
        ttsIconOff.style.display = "none";
        ttsIconOn.style.display = "block";
      } else {
        ttsBtn.classList.remove("active");
        ttsIconOn.style.display = "none";
        ttsIconOff.style.display = "block";
        if (synthesis) synthesis.cancel();
      }
    });
  }

  function speakText(text) {
    if (!ttsEnabled || !synthesis) return;
    synthesis.cancel(); // Stop current speech
    
    // Clean text from emojis or markdown
    const cleanText = text.replace(/[\u{1F600}-\u{1F6FF}]/gu, '');
    
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = currentLang === "en" ? "en-US" : "id-ID";
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    synthesis.speak(utterance);
  }

  /* =====================
     FACE DETECTION
  ===================== */
  let currentEmotion = "";
  let isCameraOn = false;
  let detectionInterval = null;
  let modelsLoaded = false;
  let emotionBuffer = [];
  let stableEmotion = "";

  const EMOTION_MAP = {
    neutral:   { label: "Netral", label_en: "Neutral", icon: "😐" },
    happy:     { label: "Senang", label_en: "Happy", icon: "😊" },
    sad:       { label: "Sedih", label_en: "Sad", icon: "😢" },
    angry:     { label: "Marah", label_en: "Angry", icon: "😠" },
    fearful:   { label: "Cemas", label_en: "Anxious", icon: "😰" },
    disgusted: { label: "Jengkel", label_en: "Annoyed", icon: "😤" },
    surprised: { label: "Terkejut", label_en: "Surprised", icon: "😮" },
    anxious:   { label: "Cemas", label_en: "Anxious", icon: "😰" }
  };

  function mapToCategory(rawEmotion) {
    const map = {
      neutral: "neutral", happy: "happy", sad: "sad",
      angry: "angry", fearful: "anxious",
      disgusted: "angry", surprised: "happy",
    };
    return map[rawEmotion] || "neutral";
  }

  async function loadFaceModels() {
    if (typeof faceapi === 'undefined') {
      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = "https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js";
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }

    const MODEL_URL = "https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@master/weights";
    try {
      await Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
        faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),
      ]);
      modelsLoaded = true;
    } catch (err) {
      console.error("Failed to load face models:", err);
    }
  }

  function resetEmotionSmoothing() {
    emotionBuffer = [];
    stableEmotion = "";
  }

  function updateFaceEmotion(category) {
    if (category === stableEmotion) return;
    stableEmotion = category;
    currentEmotion = category;
    const info = EMOTION_MAP[category] || EMOTION_MAP.neutral;
    emotionIcon.textContent = info.icon;
    emotionText.textContent = currentLang === "en" ? info.label_en : info.label;
    emotionBadge.classList.add("visible", "pulse");
    setTimeout(() => emotionBadge.classList.remove("pulse"), 450);
  }

  function shouldUpdateEmotion(category) {
    emotionBuffer.push(category);
    if (emotionBuffer.length > 4) emotionBuffer.shift();
    const count = emotionBuffer.filter(item => item === category).length;
    return count >= 3;
  }

  window.openCameraPrivacy = function() {
    const modal = document.getElementById("cameraPrivacyModal");
    if (modal) modal.style.display = "flex";
  };

  window.closeCameraPrivacy = function() {
    const modal = document.getElementById("cameraPrivacyModal");
    if (modal) modal.style.display = "none";
  };

  window.confirmCameraPrivacy = function() {
    localStorage.setItem("hm_camera_consent", "true");
    window.closeCameraPrivacy();
    startCamera(true);
  };

  async function startCamera(consentGranted = false) {
    if (isCameraOn) { stopCamera(); return; }
    if (!consentGranted && localStorage.getItem("hm_camera_consent") !== "true") {
      window.openCameraPrivacy();
      return;
    }
    try {
      cameraBtn.classList.add("loading");
      if (!modelsLoaded) await loadFaceModels();
      if (!modelsLoaded) throw new Error("Face models failed to load");

      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 320, height: 240, facingMode: "user" },
      });

      webcamVideo.srcObject = stream;
      await webcamVideo.play();

      isCameraOn = true;
      cameraBtn.classList.remove("loading");
      cameraBtn.classList.add("active");
      webcamContainer.classList.add("visible");
      resetEmotionSmoothing();

      detectionInterval = setInterval(detectEmotion, 800);
    } catch (err) {
      console.error("Camera error:", err);
      cameraBtn.classList.remove("loading");
      alert(currentLang === "en"
        ? "Could not access the camera. Please check browser permission."
        : "Tidak bisa mengakses kamera. Pastikan izin kamera sudah diberikan.");
    }
  }

  function stopCamera() {
    if (webcamVideo.srcObject) {
      webcamVideo.srcObject.getTracks().forEach(t => t.stop());
      webcamVideo.srcObject = null;
    }
    isCameraOn = false;
    cameraBtn.classList.remove("active");
    webcamContainer.classList.remove("visible");
    emotionBadge.classList.remove("visible");
    currentEmotion = "";
    resetEmotionSmoothing();
    if (detectionInterval) { clearInterval(detectionInterval); detectionInterval = null; }
  }

  async function detectEmotion() {
    if (!isCameraOn || !modelsLoaded) return;
    try {
      const result = await faceapi
        .detectSingleFace(webcamVideo, new faceapi.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.4 }))
        .withFaceExpressions();

      if (result) {
        const entries = Object.entries(result.expressions);
        entries.sort((a, b) => b[1] - a[1]);
        const [rawEmotion, confidence] = entries[0];

        if (confidence > 0.45) {
          const category = mapToCategory(rawEmotion);
          if (shouldUpdateEmotion(category)) {
            updateFaceEmotion(category);
          }
        }
      }
    } catch (err) {}
  }

  if (cameraBtn) cameraBtn.addEventListener("click", () => startCamera());
  if (webcamClose) webcamClose.addEventListener("click", stopCamera);

  /* =====================
     SPEECH-TO-TEXT
  ===================== */
  const micBtn = document.getElementById("micBtn");
  const voiceStatus = document.getElementById("voiceStatus");
  const voiceLabel = voiceStatus ? voiceStatus.querySelector(".voice-label") : null;
  const voiceDraft = document.getElementById("voiceDraft");
  const voiceDraftText = document.getElementById("voiceDraftText");
  const voiceSendBtn = document.getElementById("voiceSendBtn");
  const voiceClearBtn = document.getElementById("voiceClearBtn");
  let isListening = false;
  let accumulatedTranscript = "";
  let finalTranscript = "";
  let silenceTimer = null;
  let pendingVoiceDraft = false;

  function setVoiceStatus(textKey) {
    if (voiceLabel) voiceLabel.textContent = getI18n(textKey);
  }

  function setVoiceDraft(text) {
    const clean = text.trim();
    if (!clean) return;
    pendingVoiceDraft = true;
    input.value = clean;
    if (voiceDraft && voiceDraftText) {
      voiceDraftText.textContent = getI18n("voice_ready");
      voiceDraft.style.display = "flex";
    }
    input.focus();
  }

  function clearVoiceDraft() {
    pendingVoiceDraft = false;
    if (voiceDraft) voiceDraft.style.display = "none";
  }

  function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      if (micBtn) micBtn.style.display = "none";
      return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = currentLang === "en" ? "en-US" : "id-ID";
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      isListening = true;
      micBtn.classList.add("active");
      if (voiceStatus) voiceStatus.classList.add("visible");
      setVoiceStatus("listening");
      input.placeholder = getI18n("listening");
    };

    recognition.onresult = (event) => {
      clearTimeout(silenceTimer);
      finalTranscript = "";
      for (let i = 0; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        }
      }
      
      silenceTimer = setTimeout(() => {
        let fullText = (accumulatedTranscript + " " + finalTranscript).trim();
        if (fullText) {
          stopListening();
          setVoiceDraft(fullText);
        }
      }, 2500);
    };

    recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      setVoiceStatus("voice_error");
      if (["not-allowed", "service-not-allowed", "audio-capture"].includes(event.error)) {
        stopListening();
      }
    };
    
    recognition.onend = () => {
      if (isListening) {
        if (finalTranscript) {
          accumulatedTranscript += " " + finalTranscript;
          finalTranscript = "";
        }
        try { recognition.start(); } catch (e) { stopListening(); }
      }
    };
  }

  function startListening() {
    if (isListening) { 
      let fullText = (accumulatedTranscript + " " + finalTranscript).trim();
      stopListening(); 
      if (fullText) {
        setVoiceDraft(fullText);
      }
      return; 
    }
    
    if (!recognition) initSpeechRecognition();
    if (!recognition) return;
    
    if (synthesis) synthesis.cancel();

    accumulatedTranscript = "";
    finalTranscript = "";
    clearVoiceDraft();
    try { recognition.start(); } catch (e) { console.error(e); }
  }

  function stopListening() {
    isListening = false;
    clearTimeout(silenceTimer);
    if (recognition) {
      try { recognition.stop(); } catch (e) {}
    }
    micBtn.classList.remove("active");
    if (voiceStatus) voiceStatus.classList.remove("visible");
    input.placeholder = getI18n("input_placeholder");
  }

  if (micBtn) micBtn.addEventListener("click", startListening);
  if (voiceSendBtn) voiceSendBtn.addEventListener("click", () => sendMessage(null, true));
  if (voiceClearBtn) voiceClearBtn.addEventListener("click", () => {
    input.value = "";
    clearVoiceDraft();
    startListening();
  });
  initSpeechRecognition();

  /* =====================
     UI & CHAT LOGIC
  ===================== */
  function updateHero() {
    const show = !activeChat || !activeChat.messages || activeChat.messages.length === 0;
=======

  let chats = JSON.parse(localStorage.getItem("chats") || "[]");
  let activeChat = null;
  let isSending = false;
  let currentMood = null;

  /* =====================
     JOURNAL PROMPTS
  ===================== */
  const JOURNAL_PROMPTS = [
    "Apa 3 hal yang bikin kamu bersyukur hari ini?",
    "Kalau bisa ngomong sama diri sendiri 5 tahun lalu, apa yang mau kamu bilang?",
    "Apa yang bikin kamu senyum minggu ini?",
    "Momen terakhir kamu ngerasa benar-benar tenang itu kapan?",
    "Apa kebiasaan yang pengen banget kamu ubah, dan kenapa?",
    "Siapa orang yang paling bikin kamu ngerasa aman?",
    "Kalau hari ini adalah hari terakhir, apa yang paling kamu syukuri?",
    "Apa ketakutan terbesarmu saat ini, dan kenapa?",
    "Hal apa yang sering kamu hindari tapi sebetulnya penting?",
    "Tuliskan satu hal baik tentang dirimu yang sering kamu lupakan.",
    "Apa yang bikin kamu semangat bangun pagi?",
    "Kalau bisa traveling ke mana aja, ke mana kamu pengen pergi dan kenapa?",
    "Apa pencapaian kecil yang kamu banggakan tapi jarang diceritain?",
    "Gimana perasaanmu sekarang, kalau harus dijelasin pakai warna?",
    "Apa satu keputusan yang kalau bisa diulang, kamu mau ubah?"
  ];

  /* =====================
     MENTAL HEALTH TIPS
  ===================== */
  const TIPS = [
    { icon: "🧘", title: "Meditasi 5 Menit", desc: "Duduk tenang, fokus ke napas selama 5 menit." },
    { icon: "🚶", title: "Jalan Kaki", desc: "15 menit jalan di luar bisa ningkatin mood." },
    { icon: "💤", title: "Sleep Hygiene", desc: "Matikan layar 1 jam sebelum tidur." },
    { icon: "📝", title: "Journaling", desc: "Tulis 3 hal yang kamu syukuri setiap hari." },
    { icon: "🎵", title: "Music Therapy", desc: "Dengerin musik favorit 10 menit aja." },
    { icon: "💧", title: "Hidrasi", desc: "Minum air putih cukup tiap hari." },
    { icon: "🤝", title: "Koneksi Sosial", desc: "Hubungi teman atau keluarga, ngobrol." },
    { icon: "🌿", title: "Nature Break", desc: "Habiskan waktu di alam 10 menit." }
  ];

  /* =====================
     HELPERS
  ===================== */
  function formatTime(date) {
    return new Date(date).toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" });
  }

  function save() {
    localStorage.setItem("chats", JSON.stringify(chats));
  }

  function isMobile() {
    return window.innerWidth <= 768;
  }

  /* =====================
     HERO
  ===================== */
  function updateHero() {
    const show = !activeChat || activeChat.messages.length === 0;
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
    hero.style.display = show ? "flex" : "none";
    chat.style.display = show ? "none" : "flex";
  }

<<<<<<< HEAD
  function renderChat() {
    chat.innerHTML = "";
    if (!activeChat || !activeChat.messages) return;

    activeChat.messages.forEach((m, i) => {
      const div = document.createElement("div");
      div.className = `message ${m.role}`;
      if (m.is_voice && m.role === "user") {
        div.innerHTML = `<span style="font-size: 0.8em; opacity: 0.7;">🎤 Pesan Suara:</span><br/>${m.text}`;
      } else {
        div.innerText = m.text;
      }
      div.style.animationDelay = `${Math.min(i * 0.03, 0.3)}s`;
      chat.appendChild(div);
    });

    requestAnimationFrame(() => chat.scrollTop = chat.scrollHeight);
  }

  function showTyping() {
    if (document.getElementById("typing-indicator")) return;
    const typing = document.createElement("div");
    typing.id = "typing-indicator";
    typing.className = "typing";
    typing.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
    chat.appendChild(typing);
=======
  /* =====================
     RENDER CHAT
  ===================== */
  function renderChat() {
    chat.innerHTML = "";
    if (!activeChat) return;

    activeChat.messages.forEach((m) => {
      const wrap = document.createElement("div");
      wrap.className = `message-wrap ${m.role === "user" ? "user-wrap" : "bot-wrap"}`;

      const avatar = document.createElement("div");
      avatar.className = `msg-avatar ${m.role === "user" ? "user-avatar" : "bot-avatar"}`;
      avatar.textContent = m.role === "user" ? "👤" : "💭";

      const body = document.createElement("div");
      body.className = "msg-body";

      const bubble = document.createElement("div");
      const cls = m.role === "user" ? "user" : "bot";
      bubble.className = `message ${cls}${m.isError ? " error-msg" : ""}`;
      bubble.innerText = m.text;

      const time = document.createElement("div");
      time.className = "msg-time";
      time.textContent = m.time ? formatTime(m.time) : "";

      body.appendChild(bubble);
      body.appendChild(time);
      wrap.appendChild(avatar);
      wrap.appendChild(body);
      chat.appendChild(wrap);
    });

    requestAnimationFrame(() => { chat.scrollTop = chat.scrollHeight; });
  }

  /* =====================
     TYPING INDICATOR
  ===================== */
  function showTyping() {
    if (document.getElementById("typing-indicator")) return;
    const wrap = document.createElement("div");
    wrap.id = "typing-indicator";
    wrap.className = "typing-wrap";
    const avatar = document.createElement("div");
    avatar.className = "msg-avatar bot-avatar";
    avatar.textContent = "💭";
    const typing = document.createElement("div");
    typing.className = "typing";
    typing.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    wrap.appendChild(avatar);
    wrap.appendChild(typing);
    chat.appendChild(wrap);
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
    chat.scrollTop = chat.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById("typing-indicator");
    if (t) t.remove();
  }

<<<<<<< HEAD
  async function streamText(fullText, target) {
    let buffer = "";
    const speed = Math.max(8, Math.min(20, 800 / fullText.length));
=======
  /* =====================
     STREAMING TEXT
  ===================== */
  async function streamText(fullText, target) {
    let buffer = "";
    const speed = Math.max(6, Math.min(18, 600 / fullText.length));
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
    for (let i = 0; i < fullText.length; i++) {
      buffer += fullText[i];
      target.innerText = buffer;
      chat.scrollTop = chat.scrollHeight;
      await new Promise(r => setTimeout(r, speed));
    }
  }

<<<<<<< HEAD
  async function loadHistory() {
    try {
      const data = await apiFetch("/chats");
      chats = data || [];
      renderHistory();
      if (chats.length > 0) {
        await loadChat(chats[0].id);
      }
    } catch(e) { console.error(e); }
  }

  async function loadChat(chatId) {
    textEmotionBadge.style.display = "none";
    try {
      const msgs = await apiFetch(`/chats/${chatId}/messages`);
      const chatInfo = chats.find(c => c.id === chatId);
      activeChat = { ...chatInfo, messages: msgs, is_locked: false };
      updateUIState();
      renderChat(); updateHero(); renderHistory();
    } catch(e) { console.error(e); }
  }

  function renderHistory() {
    historyDiv.innerHTML = "";
    chats.forEach(chatItem => {
      const row = document.createElement("div");
      row.className = "history-item" + (activeChat && activeChat.id === chatItem.id ? " active" : "");
=======
  /* =====================
     SIDEBAR HISTORY
  ===================== */
  function renderHistory() {
    historyDiv.innerHTML = "";
    const sorted = [...chats].reverse();
    sorted.forEach(chatItem => {
      const row = document.createElement("div");
      row.className = "history-item" + (chatItem === activeChat ? " active" : "");
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0

      const titleBtn = document.createElement("button");
      titleBtn.className = "history-btn";
      titleBtn.textContent = chatItem.title;
<<<<<<< HEAD
      titleBtn.onclick = () => loadChat(chatItem.id);
=======
      titleBtn.onclick = () => {
        activeChat = chatItem;
        renderChat(); updateHero(); renderHistory();
        closeMobileSidebar();
      };
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0

      const renameBtn = document.createElement("button");
      renameBtn.className = "history-action";
      renameBtn.innerHTML = "✏️";
<<<<<<< HEAD
      renameBtn.onclick = async (e) => {
        e.stopPropagation();
        const name = prompt(getI18n("rename_prompt"), chatItem.title);
        if (name && name.trim()) {
          try {
            await apiFetch(`/chats/${chatItem.id}`, {
              method: "PUT",
              body: JSON.stringify({ title: name.trim() })
            });
            chatItem.title = name.trim();
            if (activeChat && activeChat.id === chatItem.id) activeChat.title = name.trim();
            renderHistory();
          } catch(err) { console.error(err); }
        }
=======
      renameBtn.onclick = e => {
        e.stopPropagation();
        const name = prompt("Rename chat:", chatItem.title);
        if (name && name.trim()) { chatItem.title = name.trim(); save(); renderHistory(); }
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
      };

      const deleteBtn = document.createElement("button");
      deleteBtn.className = "history-action delete";
      deleteBtn.innerHTML = "🗑️";
<<<<<<< HEAD
      deleteBtn.onclick = async (e) => {
        e.stopPropagation();
        if (!confirm(getI18n("delete_confirm"))) return;
        try {
          await apiFetch(`/chats/${chatItem.id}`, { method: "DELETE" });
          chats = chats.filter(c => c.id !== chatItem.id);
          if (activeChat && activeChat.id === chatItem.id) {
            if(chats.length > 0) await loadChat(chats[0].id);
            else { activeChat = null; renderChat(); updateHero(); }
          }
          renderHistory();
        } catch(err) { console.error(err); }
=======
      deleteBtn.onclick = e => {
        e.stopPropagation();
        if (!confirm("Hapus obrolan ini?")) return;
        chats = chats.filter(c => c !== chatItem);
        if (activeChat === chatItem) activeChat = chats.length > 0 ? chats[chats.length - 1] : null;
        save(); renderChat(); updateHero(); renderHistory();
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
      };

      row.append(titleBtn, renameBtn, deleteBtn);
      historyDiv.appendChild(row);
    });
  }

<<<<<<< HEAD
  async function sendMessage(text = null, isVoice = false) {
    if (activeChat && activeChat.is_locked) return;
    const msg = text ?? input.value.trim();
    if (!msg || isSending) return;

=======
  /* =====================
     SEND MESSAGE
  ===================== */
  async function sendMessage(text) {
    if (!text.trim() || isSending) return;
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
    isSending = true;
    sendBtn.disabled = true;

    if (!activeChat) {
<<<<<<< HEAD
      activeChat = { title: getI18n("new_chat_title"), messages: [] };
    }

    activeChat.messages.push({ role: "user", text: msg, is_voice: isVoice });
    clearVoiceDraft();
    input.value = "";
    renderChat(); updateHero();
    showTyping();

    try {
      const body = { message: msg, language: currentLang };
      if (activeChat.id) body.chat_id = activeChat.id;
      if (currentEmotion) body.face_emotion = currentEmotion;
      if (isVoice) body.is_voice = true;

      const res = await apiFetch("/chat", {
        method: "POST",
        body: JSON.stringify(body)
      });

      removeTyping();

      // Update chat ID if new
      if (!activeChat.id && res.chat_id) {
        activeChat.id = res.chat_id;
        // Reload history so it shows up in sidebar
        const historyData = await apiFetch("/chats");
        chats = historyData || [];
        renderHistory();
      }

      // Show Text Emotion
      if (res.text_emotion && res.text_emotion.emotion) {
        const tEmo = res.text_emotion.emotion;
        const info = EMOTION_MAP[tEmo] || EMOTION_MAP.neutral;
        textEmotionIcon.textContent = info.icon;
        textEmotionText.textContent = currentLang === "en" ? info.label_en : info.label;
        textEmotionBadge.style.display = "flex";
        textEmotionBadge.className = `emotion-badge text-emotion ${tEmo}`;
      }

      const bubble = document.createElement("div");
      bubble.className = "message bot";
      bubble.innerText = "";
      chat.appendChild(bubble);

      const botMsg = { role: "bot", text: "" };
      activeChat.messages.push(botMsg);

      await streamText(res.reply || getI18n("default_reply"), bubble);
      botMsg.text = bubble.innerText;
      
      // Handle jailbreak/locked state
      if (res.locked) {
        activeChat.is_locked = true;
        updateUIState();
      }

      speakText(res.reply);

    } catch (err) {
      console.error(err);
      removeTyping();
      activeChat.messages.push({ role: "bot", text: getI18n("error_reply") });
      renderChat();
=======
      startNewChat();
    }

    const userTime = new Date().toISOString();
    activeChat.messages.push({ role: "user", text: text.trim(), time: userTime });
    if (activeChat.messages.length === 1) {
      activeChat.title = text.trim().slice(0, 30) + (text.length > 30 ? "..." : "");
    }
    save();
    renderChat();
    updateHero();
    renderHistory();
    input.value = "";
    showTyping();

    try {
      const historyForAPI = activeChat.messages.map(m => ({ role: m.role === "user" ? "user" : "assistant", text: m.text }));
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text.trim(), history: historyForAPI, mood: currentMood })
      });
      const data = await res.json();
      removeTyping();

      const wrap = document.createElement("div");
      wrap.className = "message-wrap bot-wrap";
      const avatar = document.createElement("div");
      avatar.className = "msg-avatar bot-avatar";
      avatar.textContent = "💭";
      const bodyDiv = document.createElement("div");
      bodyDiv.className = "msg-body";
      const bubble = document.createElement("div");
      bubble.className = "message bot";
      bodyDiv.appendChild(bubble);
      const timeEl = document.createElement("div");
      timeEl.className = "msg-time";
      timeEl.textContent = formatTime(new Date().toISOString());
      bodyDiv.appendChild(timeEl);
      wrap.appendChild(avatar);
      wrap.appendChild(bodyDiv);
      chat.appendChild(wrap);

      const botTime = new Date().toISOString();
      const botMsg = { role: "bot", text: "", time: botTime };
      activeChat.messages.push(botMsg);

      await streamText(data.reply || "Hmm, coba ulangi ya.", bubble);
      botMsg.text = bubble.innerText;
      save(); renderHistory();
    } catch (err) {
      console.error("Chat error:", err);
      removeTyping();
      activeChat.messages.push({ role: "bot", text: "Maaf, lagi ada gangguan teknis. Coba lagi ya. 🔄", time: new Date().toISOString(), isError: true });
      renderChat(); save();
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
    } finally {
      isSending = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

<<<<<<< HEAD
  function updateUIState() {
    if (activeChat && activeChat.is_locked) {
      input.disabled = true;
      sendBtn.disabled = true;
      if (micBtn) micBtn.style.display = "none";
      input.placeholder = getI18n("locked") || "Obrolan dikunci. Silakan mulai obrolan baru.";
    } else {
      input.disabled = false;
      sendBtn.disabled = false;
      if (micBtn) micBtn.style.display = "flex";
      input.placeholder = getI18n("input_placeholder");
    }
  }

  sendBtn.onclick = () => sendMessage(null, pendingVoiceDraft);
  window.sendQuick = t => sendMessage(t);

  input.addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(null, pendingVoiceDraft);
    }
  });

  newChatBtn.onclick = () => {
    activeChat = { title: getI18n("new_chat_title"), messages: [], is_locked: false };
    textEmotionBadge.style.display = "none";
    updateUIState();
    renderChat(); updateHero(); renderHistory();
    input.focus();
  };

  /* =====================
     SIDEBAR TOGGLE
  ===================== */
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebarToggle");
  const mobileSidebarToggle = document.getElementById("mobileSidebarToggle");

  if (sidebar && sidebarToggle) {
    sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("collapsed"));
  }
  if (sidebar && mobileSidebarToggle) {
    mobileSidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("mobile-open");
    });
  }

  // Init
  loadHistory();
  input.focus();

  /* =====================
     SETTINGS MODAL
  ===================== */
  window.openSettings = function() {
    const modal = document.getElementById("settingsModal");
    if (!modal) return;
    document.getElementById("aiNameInput").value = userData.ai_name || "";
    document.getElementById("aiPersonaInput").value = userData.ai_persona || "";
    modal.style.display = "flex";
  };

  window.closeSettings = function() {
    const modal = document.getElementById("settingsModal");
    if (modal) modal.style.display = "none";
  };

  window.saveSettings = async function() {
    const ai_name = document.getElementById("aiNameInput").value.trim();
    const ai_persona = document.getElementById("aiPersonaInput").value.trim();
    
    const body = { language: currentLang };
    if (ai_name) body.ai_name = ai_name;
    if (ai_persona) body.ai_persona = ai_persona;

    try {
      const res = await fetch("/auth/settings", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });
      if (!res.ok) throw new Error("Failed to save settings");
      const data = await res.json();
      userData.ai_name = data.ai_name;
      userData.ai_persona = data.ai_persona;
      localStorage.setItem("hm_user", JSON.stringify(userData));
      closeSettings();
    } catch(e) { console.error(e); alert("Failed to save settings"); }
  };
=======
  /* =====================
     MOOD CHECK-IN
  ===================== */
  document.querySelectorAll(".mood-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const mood = btn.dataset.mood;
      document.querySelectorAll(".mood-btn").forEach(b => b.classList.remove("selected"));
      btn.classList.add("selected");
      currentMood = mood;
      try { await fetch("/mood", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mood }) }); } catch (e) { }
    });
  });

  /* =====================
     PROMPT CARDS
  ===================== */
  window.sendQuick = function (text) {
    if (!activeChat) startNewChat();
    input.value = text;
    sendMessage(text);
  };

  /* =====================
     SIDEBAR MOBILE
  ===================== */
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const layoutDiv = document.querySelector(".layout");

  // Remove any leftover collapsed state
  sidebar.classList.remove("collapsed");
  document.body.classList.remove("sidebar-collapsed");

  // Fix sidebar for current screen size
  function fixSidebarForScreen() {
    if (isMobile()) {
      // Mobile: sidebar off-screen, layout full width
      sidebar.style.width = "280px";
      sidebar.style.transform = "translateX(-100%)";
      if (layoutDiv) layoutDiv.style.marginLeft = "0";
    } else {
      // Desktop: sidebar always visible
      sidebar.style.width = "260px";
      sidebar.style.transform = "none";
      if (layoutDiv) layoutDiv.style.marginLeft = "260px";
    }
  }

  function openMobileSidebar() {
    sidebar.style.transform = "translateX(0)";
    sidebar.style.boxShadow = "12px 0 48px rgba(0,0,0,0.5)";
    sidebar.classList.add("mobile-open");
    sidebarOverlay.classList.add("active");
  }

  function closeMobileSidebar() {
    sidebar.style.transform = "translateX(-100%)";
    sidebar.style.boxShadow = "4px 0 24px rgba(0,0,0,0.3)";
    sidebar.classList.remove("mobile-open");
    sidebarOverlay.classList.remove("active");
  }

  if (sidebarOverlay) sidebarOverlay.addEventListener("click", closeMobileSidebar);

  const mobileMenuBtn = document.getElementById("mobileMenuBtn");
  if (mobileMenuBtn) mobileMenuBtn.addEventListener("click", openMobileSidebar);

  const mobileNewChatBtn = document.getElementById("mobileNewChatBtn");
  if (mobileNewChatBtn) mobileNewChatBtn.addEventListener("click", () => { startNewChat(); });

  // Sidebar toggle — only close on mobile
  const sidebarToggle = document.getElementById("sidebarToggle");
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      if (isMobile()) closeMobileSidebar();
    });
  }

  // Fix sidebar on resize
  window.addEventListener("resize", fixSidebarForScreen);
  fixSidebarForScreen();

  // Mobile header visibility
  const mobileHeader = document.getElementById("mobileHeader");
  function updateMobileHeader() {
    if (mobileHeader) mobileHeader.style.display = isMobile() ? "flex" : "none";
  }
  window.addEventListener("resize", updateMobileHeader);
  updateMobileHeader();

  /* =====================
     BOTTOM NAV
  ===================== */
  const navHistory = document.getElementById("navHistory");
  const navJournal = document.getElementById("navJournal");
  const navFeatures = document.getElementById("navFeatures");
  const navTips = document.getElementById("navTips");
  const allNavItems = document.querySelectorAll(".nav-item");

  function setActiveNav(btn) {
    allNavItems.forEach(n => n.classList.remove("active"));
    if (btn) btn.classList.add("active");
  }

  function clearActiveNav() {
    allNavItems.forEach(n => n.classList.remove("active"));
  }

  if (navHistory) navHistory.addEventListener("click", () => {
    setActiveNav(navHistory);
    openHistoryModal();
  });

  if (navJournal) navJournal.addEventListener("click", () => {
    setActiveNav(navJournal);
    randomJournalPrompt();
    document.getElementById("journalModal").classList.add("active");
  });

  if (navFeatures) navFeatures.addEventListener("click", () => {
    setActiveNav(navFeatures);
    document.getElementById("breathingModal").classList.add("active");
  });

  if (navTips) navTips.addEventListener("click", () => {
    setActiveNav(navTips);
    renderTips();
    document.getElementById("tipsModal").classList.add("active");
  });

  /* =====================
     HISTORY MODAL
  ===================== */
  const historyModal = document.getElementById("historyModal");
  const historyModalList = document.getElementById("historyModalList");
  const closeHistoryModal = document.getElementById("closeHistoryModal");
  const historyNewChatBtn = document.getElementById("historyNewChatBtn");

  function openHistoryModal() {
    renderHistoryModal();
    if (historyModal) historyModal.classList.add("active");
  }

  function closeHistoryModalFn() {
    if (historyModal) historyModal.classList.remove("active");
    clearActiveNav();
  }

  function renderHistoryModal() {
    if (!historyModalList) return;
    historyModalList.innerHTML = "";
    const sorted = [...chats].reverse();

    sorted.forEach(chatItem => {
      const row = document.createElement("div");
      row.className = "history-item" + (chatItem === activeChat ? " active" : "");

      const titleBtn = document.createElement("button");
      titleBtn.className = "history-btn";
      titleBtn.textContent = chatItem.title;
      titleBtn.onclick = () => {
        activeChat = chatItem;
        renderChat(); updateHero(); renderHistory();
        closeHistoryModalFn();
      };

      const renameBtn = document.createElement("button");
      renameBtn.className = "history-action";
      renameBtn.innerHTML = "✏️";
      renameBtn.onclick = e => {
        e.stopPropagation();
        const name = prompt("Rename:", chatItem.title);
        if (name && name.trim()) { chatItem.title = name.trim(); save(); renderHistoryModal(); renderHistory(); }
      };

      const deleteBtn = document.createElement("button");
      deleteBtn.className = "history-action delete";
      deleteBtn.innerHTML = "🗑️";
      deleteBtn.onclick = e => {
        e.stopPropagation();
        if (!confirm("Hapus obrolan ini?")) return;
        chats = chats.filter(c => c !== chatItem);
        if (activeChat === chatItem) activeChat = chats.length > 0 ? chats[chats.length - 1] : null;
        save(); renderChat(); updateHero(); renderHistoryModal(); renderHistory();
      };

      row.append(titleBtn, renameBtn, deleteBtn);
      historyModalList.appendChild(row);
    });
  }

  if (closeHistoryModal) closeHistoryModal.addEventListener("click", closeHistoryModalFn);
  if (historyModal) historyModal.addEventListener("click", e => { if (e.target === historyModal) closeHistoryModalFn(); });
  if (historyNewChatBtn) historyNewChatBtn.addEventListener("click", () => { startNewChat(); closeHistoryModalFn(); });

  /* =====================
     NEW CHAT
  ===================== */
  function startNewChat() {
    activeChat = { id: Date.now(), title: "Obrolan Baru", messages: [] };
    chats.push(activeChat);
    currentMood = null;
    document.querySelectorAll(".mood-btn").forEach(b => b.classList.remove("selected"));
    save(); renderChat(); updateHero(); renderHistory();
    closeMobileSidebar();
    input.focus();
  }

  if (newChatBtn) newChatBtn.addEventListener("click", startNewChat);

  /* =====================
     BREATHING EXERCISE
  ===================== */
  const breathingModal = document.getElementById("breathingModal");
  const closeBreathingModal = document.getElementById("closeBreathingModal");
  const breathingCircle = document.getElementById("breathingCircle");
  const breathingText = document.getElementById("breathingText");
  const breathingTimer = document.getElementById("breathingTimer");
  const startBreathingBtn = document.getElementById("startBreathingBtn");
  const breathingCycles = document.getElementById("breathingCycles");
  let breathingInterval = null;

  if (closeBreathingModal) closeBreathingModal.addEventListener("click", () => {
    breathingModal.classList.remove("active");
    stopBreathing();
    clearActiveNav();
  });
  if (breathingModal) breathingModal.addEventListener("click", e => {
    if (e.target === breathingModal) { breathingModal.classList.remove("active"); stopBreathing(); clearActiveNav(); }
  });

  // Sidebar breathing button
  const breathingBtn = document.getElementById("breathingBtn");
  if (breathingBtn) breathingBtn.addEventListener("click", () => breathingModal.classList.add("active"));

  function stopBreathing() {
    if (breathingInterval) { clearInterval(breathingInterval); breathingInterval = null; }
    breathingCircle.className = "breathing-circle";
    breathingText.textContent = "Mulai";
    breathingTimer.textContent = "";
    startBreathingBtn.disabled = false;
    startBreathingBtn.textContent = "Mulai Latihan";
    breathingCycles.textContent = "";
  }

  if (startBreathingBtn) {
    startBreathingBtn.addEventListener("click", () => {
      startBreathingBtn.disabled = true;
      startBreathingBtn.textContent = "Sedang berlangsung...";
      let cycle = 0;
      const totalCycles = 3;

      function runPhase(text, className, duration) {
        return new Promise(resolve => {
          breathingText.textContent = text;
          breathingCircle.className = "breathing-circle " + className;
          let remaining = duration;
          breathingTimer.textContent = remaining;
          breathingInterval = setInterval(() => {
            remaining--;
            breathingTimer.textContent = remaining > 0 ? remaining : "";
            if (remaining <= 0) { clearInterval(breathingInterval); resolve(); }
          }, 1000);
        });
      }

      async function runCycle() {
        while (cycle < totalCycles) {
          cycle++;
          breathingCycles.textContent = `Siklus ${cycle} dari ${totalCycles}`;
          await runPhase("Tarik napas...", "inhale", 4);
          await runPhase("Tahan...", "hold", 7);
          await runPhase("Buang napas...", "exhale", 8);
        }
        breathingText.textContent = "Selesai! 🎉";
        breathingTimer.textContent = "";
        breathingCircle.className = "breathing-circle";
        startBreathingBtn.disabled = false;
        startBreathingBtn.textContent = "Ulangi";
        breathingCycles.textContent = "Latihan selesai!";
      }
      runCycle();
    });
  }

  /* =====================
     JOURNALING
  ===================== */
  const journalModal = document.getElementById("journalModal");
  const closeJournalModal = document.getElementById("closeJournalModal");
  const journalPromptText = document.getElementById("journalPromptText");
  const shufflePromptBtn = document.getElementById("shufflePromptBtn");
  const usePromptBtn = document.getElementById("usePromptBtn");

  function randomJournalPrompt() {
    journalPromptText.textContent = JOURNAL_PROMPTS[Math.floor(Math.random() * JOURNAL_PROMPTS.length)];
  }

  // Sidebar journal button
  const journalBtn = document.getElementById("journalBtn");
  if (journalBtn) journalBtn.addEventListener("click", () => { randomJournalPrompt(); journalModal.classList.add("active"); });

  if (closeJournalModal) closeJournalModal.addEventListener("click", () => { journalModal.classList.remove("active"); clearActiveNav(); });
  if (journalModal) journalModal.addEventListener("click", e => { if (e.target === journalModal) { journalModal.classList.remove("active"); clearActiveNav(); } });
  if (shufflePromptBtn) shufflePromptBtn.addEventListener("click", randomJournalPrompt);
  if (usePromptBtn) usePromptBtn.addEventListener("click", () => {
    journalModal.classList.remove("active");
    clearActiveNav();
    if (!activeChat) startNewChat();
    input.value = journalPromptText.textContent;
    sendMessage(journalPromptText.textContent);
  });

  /* =====================
     TIPS
  ===================== */
  const tipsModal = document.getElementById("tipsModal");
  const closeTipsModal = document.getElementById("closeTipsModal");
  const tipsGrid = document.getElementById("tipsGrid");

  function renderTips() {
    tipsGrid.innerHTML = "";
    TIPS.forEach(tip => {
      const card = document.createElement("div");
      card.className = "tip-card";
      card.innerHTML = `<span class="tip-icon">${tip.icon}</span><div class="tip-title">${tip.title}</div><div class="tip-desc">${tip.desc}</div>`;
      tipsGrid.appendChild(card);
    });
  }

  // Sidebar tips button
  const tipsBtn = document.getElementById("tipsBtn");
  if (tipsBtn) tipsBtn.addEventListener("click", () => { renderTips(); tipsModal.classList.add("active"); });

  if (closeTipsModal) closeTipsModal.addEventListener("click", () => { tipsModal.classList.remove("active"); clearActiveNav(); });
  if (tipsModal) tipsModal.addEventListener("click", e => { if (e.target === tipsModal) { tipsModal.classList.remove("active"); clearActiveNav(); } });

  /* =====================
     WELLNESS CAROUSEL
  ===================== */
  const wellnessTrack = document.getElementById("wellnessTrack");
  const wellnessDots = document.getElementById("wellnessDots");
  if (wellnessTrack && wellnessDots) {
    const cards = wellnessTrack.children;
    let currentSlide = 0;
    for (let i = 0; i < cards.length; i++) {
      const dot = document.createElement("button");
      dot.className = "wellness-dot" + (i === 0 ? " active" : "");
      dot.addEventListener("click", () => goToSlide(i));
      wellnessDots.appendChild(dot);
    }
    function goToSlide(idx) {
      currentSlide = idx;
      wellnessTrack.style.transform = `translateX(-${idx * 100}%)`;
      wellnessDots.querySelectorAll(".wellness-dot").forEach((d, i) => d.classList.toggle("active", i === idx));
    }
    setInterval(() => { goToSlide((currentSlide + 1) % cards.length); }, 6000);
  }

  /* =====================
     SEND HANDLERS
  ===================== */
  sendBtn.addEventListener("click", () => sendMessage(input.value));
  input.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(input.value); } });

  /* =====================
     INIT
  ===================== */
  if (chats.length > 0) {
    activeChat = chats[chats.length - 1];
  }
  renderChat();
  renderHistory();
  updateHero();
  randomJournalPrompt();
  input.focus();
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
});
