document.addEventListener("DOMContentLoaded", () => {
  const chat = document.getElementById("chat");
  const input = document.getElementById("input");
  const sendBtn = document.getElementById("sendBtn");
  const newChatBtn = document.getElementById("newChatBtn");
  const hero = document.getElementById("hero");
  const historyDiv = document.getElementById("history");

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
    hero.style.display = show ? "flex" : "none";
    chat.style.display = show ? "none" : "flex";
  }

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
    chat.scrollTop = chat.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById("typing-indicator");
    if (t) t.remove();
  }

  /* =====================
     STREAMING TEXT
  ===================== */
  async function streamText(fullText, target) {
    let buffer = "";
    const speed = Math.max(6, Math.min(18, 600 / fullText.length));
    for (let i = 0; i < fullText.length; i++) {
      buffer += fullText[i];
      target.innerText = buffer;
      chat.scrollTop = chat.scrollHeight;
      await new Promise(r => setTimeout(r, speed));
    }
  }

  /* =====================
     SIDEBAR HISTORY
  ===================== */
  // Custom modal helpers (replace native prompt/confirm which browsers may block)
  function showRenameModal(chatItem, callback) {
    var overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.6);z-index:9999;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);animation:fadeIn 0.15s ease';
    var box = document.createElement('div');
    box.style.cssText = 'background:linear-gradient(135deg,#1a1a3e,#12122e);border:1px solid rgba(99,102,241,0.3);border-radius:16px;padding:24px;min-width:320px;box-shadow:0 20px 60px rgba(0,0,0,0.5)';
    box.innerHTML = '<h3 style="margin:0 0 12px;color:#e0e0ff;font-size:16px">✏️ Rename Obrolan</h3>';
    var inp = document.createElement('input');
    inp.type = 'text'; inp.value = chatItem.title;
    inp.style.cssText = 'width:100%;padding:10px 14px;border-radius:10px;border:1px solid rgba(99,102,241,0.3);background:rgba(255,255,255,0.06);color:#fff;font-size:14px;outline:none;box-sizing:border-box;margin-bottom:16px';
    inp.addEventListener('focus', function () { inp.style.borderColor = '#6366f1'; });
    inp.addEventListener('blur', function () { inp.style.borderColor = 'rgba(99,102,241,0.3)'; });
    var btns = document.createElement('div');
    btns.style.cssText = 'display:flex;gap:8px;justify-content:flex-end';
    var cancelBtn = document.createElement('button');
    cancelBtn.textContent = 'Batal';
    cancelBtn.style.cssText = 'padding:8px 18px;border-radius:10px;border:1px solid rgba(255,255,255,0.15);background:transparent;color:#aaa;cursor:pointer;font-size:13px';
    var saveBtn = document.createElement('button');
    saveBtn.textContent = 'Simpan';
    saveBtn.style.cssText = 'padding:8px 18px;border-radius:10px;border:none;background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;cursor:pointer;font-size:13px;font-weight:600';
    cancelBtn.onclick = function () { document.body.removeChild(overlay); };
    saveBtn.onclick = function () { var v = inp.value.trim(); document.body.removeChild(overlay); if (v) callback(v); };
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') saveBtn.click(); if (e.key === 'Escape') cancelBtn.click(); });
    btns.append(cancelBtn, saveBtn);
    box.append(inp, btns);
    overlay.appendChild(box);
    document.body.appendChild(overlay);
    inp.focus(); inp.select();
  }

  function showDeleteModal(chatItem, callback) {
    var overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.6);z-index:9999;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px)';
    var box = document.createElement('div');
    box.style.cssText = 'background:linear-gradient(135deg,#1a1a3e,#12122e);border:1px solid rgba(248,113,113,0.3);border-radius:16px;padding:24px;min-width:300px;box-shadow:0 20px 60px rgba(0,0,0,0.5);text-align:center';
    box.innerHTML = '<h3 style="margin:0 0 8px;color:#f87171;font-size:16px">🗑️ Hapus Obrolan</h3><p style="color:#aaa;font-size:14px;margin:0 0 20px">Hapus <strong style="color:#e0e0ff">"' + chatItem.title + '"</strong>?</p>';
    var btns = document.createElement('div');
    btns.style.cssText = 'display:flex;gap:8px;justify-content:center';
    var cancelBtn = document.createElement('button');
    cancelBtn.textContent = 'Batal';
    cancelBtn.style.cssText = 'padding:8px 24px;border-radius:10px;border:1px solid rgba(255,255,255,0.15);background:transparent;color:#aaa;cursor:pointer;font-size:13px';
    var delBtn = document.createElement('button');
    delBtn.textContent = 'Hapus';
    delBtn.style.cssText = 'padding:8px 24px;border-radius:10px;border:none;background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;cursor:pointer;font-size:13px;font-weight:600';
    cancelBtn.onclick = function () { document.body.removeChild(overlay); };
    delBtn.onclick = function () { document.body.removeChild(overlay); callback(); };
    btns.append(cancelBtn, delBtn);
    box.appendChild(btns);
    overlay.appendChild(box);
    document.body.appendChild(overlay);
  }

  function renderHistory() {
    historyDiv.innerHTML = "";
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
        if (isMobile()) closeMobileSidebar();
      };

      const renameBtn = document.createElement("button");
      renameBtn.className = "history-action";
      renameBtn.innerHTML = "✏️";
      renameBtn.title = "Rename";
      renameBtn.onclick = e => {
        e.stopPropagation();
        showRenameModal(chatItem, function (name) {
          chatItem.title = name; save(); renderHistory();
        });
      };

      const deleteBtn = document.createElement("button");
      deleteBtn.className = "history-action delete";
      deleteBtn.innerHTML = "🗑️";
      deleteBtn.title = "Hapus";
      deleteBtn.onclick = e => {
        e.stopPropagation();
        showDeleteModal(chatItem, function () {
          chats = chats.filter(c => c !== chatItem);
          if (activeChat === chatItem) activeChat = chats.length > 0 ? chats[chats.length - 1] : null;
          save(); renderChat(); updateHero(); renderHistory();
        });
      };

      row.append(titleBtn, renameBtn, deleteBtn);
      historyDiv.appendChild(row);
    });
  }

  /* =====================
     SEND MESSAGE
  ===================== */
  async function sendMessage(text) {
    if (!text.trim() || isSending) return;
    isSending = true;
    sendBtn.disabled = true;

    if (!activeChat) {
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
    } finally {
      isSending = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  /* =====================
     MOOD CHECK-IN
  ===================== */
  const MOOD_PROMPTS = {
    senang: "Aku lagi senang nih! 😊",
    biasa: "Aku lagi biasa aja sih hari ini.",
    sedih: "Aku lagi sedih... 😢",
    cemas: "Aku lagi cemas banget... 😟",
    marah: "Aku lagi kesel banget... 😤"
  };

  document.querySelectorAll(".mood-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const mood = btn.dataset.mood;
      document.querySelectorAll(".mood-btn").forEach(b => b.classList.remove("selected"));
      btn.classList.add("selected");
      currentMood = mood;
      try { await fetch("/mood", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mood }) }); } catch (e) { }
      // Send mood as prompt
      const prompt = MOOD_PROMPTS[mood] || "Hai, aku mau cerita...";
      if (!activeChat) startNewChat();
      input.value = prompt;
      sendMessage(prompt);
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
     SIDEBAR — handled by inline <script> in HTML
     Only define closeMobileSidebar as no-op for calls from other places
  ===================== */
  function closeMobileSidebar() { /* no-op — sidebar hidden on mobile via CSS */ }

  const mobileNewChatBtn = document.getElementById("mobileNewChatBtn");
  if (mobileNewChatBtn) mobileNewChatBtn.addEventListener("click", () => { startNewChat(); });

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
    if (isMobile()) closeMobileSidebar();
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
});
