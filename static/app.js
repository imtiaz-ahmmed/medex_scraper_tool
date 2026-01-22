function start() {
  const s = document.getElementById("status");
  s.innerText = "Scraping... check terminal";

  fetch("/start")
    .then((r) => r.json())
    .then((d) => (s.innerText = d.status))
    .catch(() => (s.innerText = "Error occurred"));
}

function download() {
  window.location = "/download";
}
