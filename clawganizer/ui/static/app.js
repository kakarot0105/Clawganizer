(function () {
  const runBtn = document.getElementById("runBtn");
  const pendingHint = document.getElementById("pendingHint");
  const results = document.getElementById("results");
  const resultsTitle = document.getElementById("resultsTitle");
  const resultsSummary = document.getElementById("resultsSummary");
  const resultsCats = document.getElementById("resultsCats");
  const againBtn = document.getElementById("againBtn");
  const undoBtn = document.getElementById("undoBtn");
  const takeover = document.getElementById("takeover");
  const takeoverLine = document.getElementById("takeoverLine");
  const hero = document.getElementById("hero");

  const LINES = [
    "Gathering the clutter…",
    "Tornado inbound…",
    "Files caught in the swirl…",
    "Sorting by type…",
    "Landing everything clean…",
  ];

  let busy = false;
  let lineTimer = 0;

  async function fetchStatus() {
    const res = await fetch("/api/status");
    if (!res.ok) throw new Error("status failed");
    return res.json();
  }

  function setHint(text) {
    pendingHint.textContent = text;
  }

  async function refreshStatus() {
    try {
      const status = await fetchStatus();
      const n = status.pending || 0;
      if (n === 0) setHint("All clear — still fun to Run");
      else setHint(`${n} loose file${n === 1 ? "" : "s"} ready`);
      return status;
    } catch {
      setHint("Local UI ready");
      return null;
    }
  }

  function showTakeover(on) {
    takeover.classList.toggle("is-active", on);
  }

  function cycleLines() {
    let i = 0;
    takeoverLine.textContent = LINES[0];
    lineTimer = window.setInterval(() => {
      i = (i + 1) % LINES.length;
      takeoverLine.textContent = LINES[i];
    }, 850);
  }

  function stopLines(finalText) {
    window.clearInterval(lineTimer);
    if (finalText) takeoverLine.textContent = finalText;
  }

  function renderResults(payload) {
    results.hidden = false;
    const applied = payload.applied !== false;
    const count = payload.move_count || 0;
    if (count === 0) {
      resultsTitle.textContent = "Already tidy";
      resultsSummary.textContent = "No loose files needed moving. The tornado still looked great.";
      resultsCats.innerHTML = "";
      return;
    }
    resultsTitle.textContent = applied ? "Organized" : "Preview";
    resultsSummary.textContent = applied
      ? `Moved ${count} file${count === 1 ? "" : "s"} into clean folders.`
      : `Would move ${count} file${count === 1 ? "" : "s"}.`;
    resultsCats.innerHTML = "";
    const cats = payload.by_category || {};
    Object.keys(cats).forEach((name) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${cats[name]}</strong> ${name}`;
      resultsCats.appendChild(li);
    });
  }

  async function runOrganize() {
    if (busy) return;
    busy = true;
    runBtn.disabled = true;
    results.hidden = true;
    document.body.classList.remove("is-done");
    document.body.classList.add("is-storming");
    showTakeover(true);
    cycleLines();

    // Start tornado + organize in parallel; tornado must finish for the spectacle,
    // organize result waits until after the calm.
    const storm = window.ClawTornado.play();
    const organizePromise = fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ apply: true }),
    }).then(async (res) => {
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Organize failed");
      return data;
    });

    let payload = null;
    let error = null;
    try {
      const settled = await Promise.allSettled([storm, organizePromise]);
      if (settled[1].status === "fulfilled") payload = settled[1].value;
      else error = settled[1].reason;
      // Ensure storm completes even if organize was faster
      if (settled[0].status === "rejected") {
        // ignore animation errors
      }
    } catch (err) {
      error = err;
    }

    stopLines(error ? "Storm aborted" : "Sky clearing…");
    await sleep(500);
    window.ClawTornado.stop();
    showTakeover(false);
    document.body.classList.remove("is-storming");
    document.body.classList.add("is-done");

    if (error) {
      results.hidden = false;
      resultsTitle.textContent = "Couldn’t finish";
      resultsSummary.textContent = String(error.message || error);
      resultsCats.innerHTML = "";
    } else {
      renderResults(payload);
      hero.querySelector(".lede").textContent =
        payload.move_count > 0
          ? "The tornado did its job. Your clutter has new homes."
          : "Nothing to sweep — your Downloads and Desktop were already calm.";
    }

    await refreshStatus();
    busy = false;
    runBtn.disabled = false;
  }

  function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
  }

  async function undoLast() {
    if (busy) return;
    busy = true;
    undoBtn.disabled = true;
    try {
      const res = await fetch("/api/undo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dry_run: false }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Undo failed");
      results.hidden = false;
      resultsTitle.textContent = data.move_count ? "Restored" : "Nothing to undo";
      resultsSummary.textContent = data.move_count
        ? `Put ${data.move_count} file${data.move_count === 1 ? "" : "s"} back.`
        : (data.errors && data.errors[0]) || "No previous run to reverse.";
      resultsCats.innerHTML = "";
      await refreshStatus();
    } catch (err) {
      results.hidden = false;
      resultsTitle.textContent = "Undo failed";
      resultsSummary.textContent = String(err.message || err);
    } finally {
      busy = false;
      undoBtn.disabled = false;
    }
  }

  runBtn.addEventListener("click", runOrganize);
  againBtn.addEventListener("click", runOrganize);
  undoBtn.addEventListener("click", undoLast);

  refreshStatus();
})();
