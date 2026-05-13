/**
 * HelloMind — Login / Register Logic
 */

// Check if already logged in
const token = localStorage.getItem("hm_token");
if (token) {
  // Verify token is still valid
  fetch("/auth/me", {
    headers: { "Authorization": `Bearer ${token}` },
  })
    .then(r => {
      if (r.ok) window.location.href = "/";
    })
    .catch(() => {});
}

function switchTab(tab) {
  const loginTab = document.getElementById("loginTab");
  const registerTab = document.getElementById("registerTab");
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");
  const indicator = document.getElementById("tabIndicator");
  const msg = document.getElementById("authMessage");

  msg.className = "auth-message";
  msg.textContent = "";

  if (tab === "login") {
    loginTab.classList.add("active");
    registerTab.classList.remove("active");
    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");
    indicator.classList.remove("register");
  } else {
    registerTab.classList.add("active");
    loginTab.classList.remove("active");
    registerForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    indicator.classList.add("register");
  }
}

function showMessage(text, type = "error") {
  const msg = document.getElementById("authMessage");
  msg.textContent = text;
  msg.className = `auth-message ${type}`;
}

function setLoading(btn, loading) {
  if (loading) {
    btn.classList.add("loading");
    btn.disabled = true;
  } else {
    btn.classList.remove("loading");
    btn.disabled = false;
  }
}

async function handleLogin(e) {
  e.preventDefault();
  const btn = document.getElementById("loginSubmit");
  const username = document.getElementById("loginUsername").value.trim();
  const password = document.getElementById("loginPassword").value;

  if (!username || !password) {
    showMessage("Isi semua field ya.");
    return;
  }

  setLoading(btn, true);

  try {
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      showMessage(data.detail || "Login gagal.");
      setLoading(btn, false);
      return;
    }

    // Save token and user info
    localStorage.setItem("hm_token", data.token);
    localStorage.setItem("hm_user", JSON.stringify(data.user));

    showMessage("Berhasil masuk! Mengalihkan...", "success");
    setTimeout(() => {
      window.location.href = "/";
    }, 600);
  } catch (err) {
    showMessage("Gagal terhubung ke server.");
    setLoading(btn, false);
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const btn = document.getElementById("registerSubmit");
  const username = document.getElementById("regUsername").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value;
  const confirm = document.getElementById("regConfirm").value;

  if (!username || !email || !password || !confirm) {
    showMessage("Isi semua field ya.");
    return;
  }

  if (password !== confirm) {
    showMessage("Password tidak cocok.");
    return;
  }

  if (password.length < 4) {
    showMessage("Password minimal 4 karakter.");
    return;
  }

  setLoading(btn, true);

  try {
    const res = await fetch("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      showMessage(data.detail || "Registrasi gagal.");
      setLoading(btn, false);
      return;
    }

    // Auto-login after register
    localStorage.setItem("hm_token", data.token);
    localStorage.setItem("hm_user", JSON.stringify(data.user));

    showMessage("Akun berhasil dibuat! Mengalihkan...", "success");
    setTimeout(() => {
      window.location.href = "/";
    }, 600);
  } catch (err) {
    showMessage("Gagal terhubung ke server.");
    setLoading(btn, false);
  }
}
