let SECTION = null;
let SELECTED = new Set();
let POLLING = null;

function openModal(section) {
  SECTION = section;
  SELECTED.clear();
  document.getElementById("modal").classList.remove("hidden");
  resetUI();
  renderPad();
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
  if (POLLING) clearInterval(POLLING);
}

function resetUI() {
  document.getElementById("progressSection").classList.add("hidden");
  document.getElementById("actionButtons").classList.remove("hidden");
  document.getElementById("limitInput").style.display = "none";
  document.getElementById("limitToggle").checked = false;
  document.querySelector('input[value="ALL"]').checked = true;
  toggleMode();
}

function renderPad() {
  const pad = document.getElementById("alphabetPad");
  pad.innerHTML = "";
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").forEach((ch) => {
    const b = document.createElement("button");
    b.innerText = ch;
    b.onclick = () => {
      b.classList.toggle("active");
      SELECTED.has(ch) ? SELECTED.delete(ch) : SELECTED.add(ch);
    };
    pad.appendChild(b);
  });
}

document.getElementById("limitToggle").onchange = (e) => {
  document.getElementById("limitInput").style.display = e.target.checked
    ? "inline-block"
    : "none";
};

function toggleMode() {
  const mode = document.querySelector('input[name="scrapeMode"]:checked').value;
  const alphaContainer = document.getElementById("alphabetContainer");

  if (mode === "ALL") {
    alphaContainer.classList.add("hidden");
  } else {
    alphaContainer.classList.remove("hidden");
  }
}

function startScrape() {
  const mode = document.querySelector('input[name="scrapeMode"]:checked').value;
  let alpha = "ALL";

  if (mode === "ALPHA") {
    alpha = SELECTED.size ? [...SELECTED].join(",") : "";
    if (!alpha) {
      alert("Please select at least one alphabet!");
      return;
    }
  }

  const limit = document.getElementById("limitToggle").checked
    ? document.getElementById("limitInput").value
    : "";

  // Show Progress UI
  document.getElementById("progressSection").classList.remove("hidden");
  document.getElementById("actionButtons").classList.add("hidden");

  // Start polling
  startPolling();

  // Build query string
  let query = `/scrape?section=${SECTION}&alphabets=${alpha}&herbal=0`;
  if (limit) {
    query += `&limit=${limit}`;
  }

  fetch(query)
    .then((r) => r.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        resetUI();
        clearInterval(POLLING);
      } else {
        // Success
        clearInterval(POLLING);
        document.getElementById("progressPercent").innerText = "100%";
        document.getElementById("progressBar").style.width = "100%";
        document.getElementById("progressStatus").innerText = "Complete!";
        setTimeout(() => {
          window.location = "/download";
          closeModal();
        }, 1000);
      }
    })
    .catch(err => {
      alert("Error: " + err);
      closeModal();
    });
}

function startPolling() {
  if (POLLING) clearInterval(POLLING);
  POLLING = setInterval(() => {
    // ... existing polling ...
    fetch("/progress")
      .then(r => r.json())
      .then(data => {
        document.getElementById("progressPercent").innerText = data.percent + "%";
        document.getElementById("progressBar").style.width = data.percent + "%";

        // Also update single progress if visible
        if (!document.getElementById("singleProgressSection").classList.contains("hidden")) {
          document.getElementById("singleProgressPercent").innerText = data.percent + "%";
          document.getElementById("singleProgressBar").style.width = data.percent + "%";
          document.getElementById("singleProgressStatus").innerText = data.status;
        }

        document.getElementById("progressTime").innerText = data.estimated_remaining + " remaining";
        document.getElementById("progressStatus").innerText = `${data.status} (${data.current}/${data.total})`;
      });
  }, 1000);
}

// Search Feature
function openSearchModal() {
  document.getElementById("searchModal").classList.remove("hidden");
  document.getElementById("searchInput").focus();
}

function closeSearchModal() {
  document.getElementById("searchModal").classList.add("hidden");
}

function performSearch() {
  const q = document.getElementById("searchInput").value;
  if (!q) return;

  document.getElementById("searchResults").innerHTML = '<p style="color: #888;">Searching...</p>';

  fetch(`/search?q=${encodeURIComponent(q)}`)
    .then(r => r.json())
    .then(data => {
      const container = document.getElementById("searchResults");
      container.innerHTML = "";
      if (data.length === 0) {
        container.innerHTML = '<p>No results found.</p>';
        return;
      }

      data.forEach(item => {
        const div = document.createElement("div");
        div.className = "search-result-item";
        div.style.padding = "10px";
        div.style.background = "rgba(255,255,255,0.05)";
        div.style.marginBottom = "5px";
        div.style.borderRadius = "5px";
        div.style.cursor = "pointer";
        div.style.display = "flex";
        div.style.justifyContent = "space-between";
        div.style.alignItems = "center";

        div.innerHTML = `<span>${item.name}</span> <small style="color:#aaa;">Click to Scrape</small>`;

        div.onclick = () => scrapeSingle(item.url, item.name);

        container.appendChild(div);
      });
    });
}

function scrapeSingle(url, name) {
  if (!confirm(`Scrape details for ${name}?`)) return;

  document.getElementById("singleProgressSection").classList.remove("hidden");
  startPolling();

  fetch(`/scrape_single?url=${encodeURIComponent(url)}&name=${encodeURIComponent(name)}`)
    .then(r => r.json())
    .then(data => {
      clearInterval(POLLING);
      if (data.error) {
        alert(data.error);
      } else {
        window.location = "/download";
        closeSearchModal();
        document.getElementById("singleProgressSection").classList.add("hidden");
      }
    });
}
