/**
 * HelloMind — Mood Dashboard Logic
 */

const EMOTION_CONFIG = {
  happy:   { label: "Senang",  icon: "😊", color: "#4ade80" },
  sad:     { label: "Sedih",   icon: "😢", color: "#60a5fa" },
  angry:   { label: "Marah",   icon: "😠", color: "#f87171" },
  anxious: { label: "Cemas",   icon: "😰", color: "#fbbf24" },
  neutral: { label: "Netral",  icon: "😐", color: "#94a3b8" },
};

let trendChart = null;
let distChart = null;

// Auth check
const token = localStorage.getItem("hm_token");
if (!token) {
  window.location.href = "/login";
}

async function apiFetch(url) {
  const res = await fetch(url, {
    headers: { "Authorization": `Bearer ${token}` },
  });
  if (res.status === 401) {
    localStorage.removeItem("hm_token");
    window.location.href = "/login";
    return null;
  }
  if (!res.ok) return null;
  return res.json();
}

async function loadDashboard() {
  const days = parseInt(document.getElementById("dayRange").value);

  const [summary, history] = await Promise.all([
    apiFetch(`/mood/summary?days=${days}`),
    apiFetch(`/mood/history?days=${days}`),
  ]);

  if (!summary || !history) return;

  // Summary cards
  document.getElementById("totalEntries").textContent = summary.total_entries;

  const domEmo = EMOTION_CONFIG[summary.dominant_emotion] || EMOTION_CONFIG.neutral;
  document.getElementById("dominantEmotion").textContent = domEmo.label;
  document.getElementById("dominantIcon").textContent = domEmo.icon;
  document.getElementById("avgIntensity").textContent =
    summary.avg_intensity > 0 ? `${summary.avg_intensity}/5` : "—";

  // Trend chart
  renderTrendChart(summary.daily_moods);

  // Distribution chart
  renderDistChart(summary.emotion_counts);

  // Recent entries
  renderRecent(history.slice(0, 20));
}

function renderTrendChart(dailyMoods) {
  const ctx = document.getElementById("moodTrendChart").getContext("2d");

  const labels = dailyMoods.map(d => {
    const date = new Date(d.date);
    return date.toLocaleDateString("id-ID", { day: "numeric", month: "short" });
  });

  const intensities = dailyMoods.map(d => d.avg_intensity);
  const colors = dailyMoods.map(d => {
    const cfg = EMOTION_CONFIG[d.dominant_emotion] || EMOTION_CONFIG.neutral;
    return cfg.color;
  });

  if (trendChart) trendChart.destroy();

  trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Intensitas Mood",
        data: intensities,
        borderColor: "#818cf8",
        backgroundColor: "rgba(129, 140, 248, 0.1)",
        borderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 8,
        pointBackgroundColor: colors,
        pointBorderColor: colors,
        pointBorderWidth: 2,
        fill: true,
        tension: 0.35,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(16, 16, 44, 0.9)",
          borderColor: "rgba(99, 102, 241, 0.3)",
          borderWidth: 1,
          titleColor: "#f0f0ff",
          bodyColor: "#a0a0cc",
          cornerRadius: 10,
          padding: 12,
          callbacks: {
            label: function(ctx) {
              const dm = dailyMoods[ctx.dataIndex];
              const cfg = EMOTION_CONFIG[dm.dominant_emotion] || EMOTION_CONFIG.neutral;
              return `${cfg.icon} ${cfg.label} — Intensitas: ${dm.avg_intensity}/5 (${dm.count} entri)`;
            }
          }
        },
      },
      scales: {
        y: {
          min: 0,
          max: 5,
          ticks: {
            stepSize: 1,
            color: "#6a6a99",
            font: { family: "'Inter', sans-serif", size: 11 },
          },
          grid: { color: "rgba(99, 102, 241, 0.06)" },
          border: { display: false },
        },
        x: {
          ticks: {
            color: "#6a6a99",
            font: { family: "'Inter', sans-serif", size: 11 },
            maxRotation: 45,
          },
          grid: { display: false },
          border: { display: false },
        },
      },
    },
  });
}

function renderDistChart(emotionCounts) {
  const ctx = document.getElementById("emotionDistChart").getContext("2d");

  const emotions = Object.keys(emotionCounts);
  const counts = Object.values(emotionCounts);
  const labels = emotions.map(e => (EMOTION_CONFIG[e] || EMOTION_CONFIG.neutral).label);
  const colors = emotions.map(e => (EMOTION_CONFIG[e] || EMOTION_CONFIG.neutral).color);

  if (distChart) distChart.destroy();

  if (emotions.length === 0) {
    // Show empty state
    return;
  }

  distChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: counts,
        backgroundColor: colors.map(c => c + "33"),
        borderColor: colors,
        borderWidth: 2,
        hoverBorderWidth: 3,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "60%",
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#a0a0cc",
            font: { family: "'Inter', sans-serif", size: 12 },
            padding: 16,
            usePointStyle: true,
            pointStyleWidth: 10,
          },
        },
        tooltip: {
          backgroundColor: "rgba(16, 16, 44, 0.9)",
          borderColor: "rgba(99, 102, 241, 0.3)",
          borderWidth: 1,
          titleColor: "#f0f0ff",
          bodyColor: "#a0a0cc",
          cornerRadius: 10,
          padding: 12,
        },
      },
    },
  });
}

function renderRecent(entries) {
  const list = document.getElementById("recentList");

  if (!entries || entries.length === 0) {
    list.innerHTML = `<div class="recent-empty">Belum ada data mood. Mulai ngobrol di chat untuk merekam mood!</div>`;
    return;
  }

  list.innerHTML = entries.map(e => {
    const cfg = EMOTION_CONFIG[e.emotion] || EMOTION_CONFIG.neutral;
    const date = new Date(e.created_at);
    const timeStr = date.toLocaleString("id-ID", {
      day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
    });

    const intensityDots = Array.from({ length: 5 }, (_, i) =>
      `<div class="intensity-dot ${i < e.intensity ? 'active' : ''}"></div>`
    ).join("");

    return `
      <div class="recent-item">
        <span class="recent-emoji">${cfg.icon}</span>
        <div class="recent-info">
          <div class="recent-note">${escapeHtml(e.note || "—")}</div>
          <div class="recent-meta">
            <span class="recent-badge ${e.emotion}">${cfg.label}</span>
            <div class="recent-intensity">${intensityDots}</div>
            <span>${timeStr}</span>
            <span>•</span>
            <span>${e.source}</span>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Events
document.getElementById("dayRange").addEventListener("change", loadDashboard);

// Init
loadDashboard();
