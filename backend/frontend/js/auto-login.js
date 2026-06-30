// Auto-login with demo account — run this BEFORE other scripts
// so the token is always available without manual login.
(async function autoLogin() {
  const existingToken = localStorage.getItem("token");
  if (existingToken) {
    return; // Token already present, no need to re-fetch
  }

  try {
    const res = await fetch("/auth/auto-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    if (!res.ok) {
      console.warn("[Auto-Login] Failed to get demo token:", res.status);
      return;
    }

    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      console.log("[Auto-Login] Demo token obtained successfully");
    }
  } catch (err) {
    console.warn("[Auto-Login] Error:", err.message);
  }
})();