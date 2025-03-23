// Ensure Socket.IO is properly connected
const socket = io({ transports: ["websocket"] });

function startMonitoring() {
  const urlInput = document.getElementById("site-url");
  const url = urlInput.value.trim();

  if (url) {
    addStatusMessage(url, "initializing", "Initializing monitoring...");
    socket.emit("start_monitoring", { url });
    urlInput.value = "";
  } else {
    console.error("❌ Please enter a valid URL.");
  }
}

function addStatusMessage(url, status, message) {
  const statusList = document.getElementById("status-list");
  console.log(document.getElementById("status-list"));


  if (!statusList) {
    console.error("❌ status-list element not found!");
    return;
  }

  const statusItem = document.createElement("div");
  statusItem.className = `status-item ${status}`;
  statusItem.innerHTML = `
        <div class="status-content">
            <strong>${url}</strong>: ${message}
        </div>
        <div class="timestamp">
            ${new Date().toLocaleTimeString()}
        </div>
    `;

  statusList.insertBefore(statusItem, statusList.firstChild);

  while (statusList.children.length > 10) {
    statusList.removeChild(statusList.lastChild);
  }
}

// WebSocket Connection
socket.on("connect", () => {
  console.log("✅ Connected to WebSocket server");
});

// Handling status updates
socket.on("status_update", (data) => {
  console.log("Received status update:", data);
  const statusList = document.getElementById("status-list");

  if (!statusList) {
    console.error("❌ status-list element not found!");
    return;
  }

  data.sites.forEach((site) => {
    const existing = Array.from(statusList.children).find(
      (el) => el.querySelector("strong").textContent === site.url
    );

    const statusElement = document.createElement("div");
    statusElement.className = `status-item ${site.status.toLowerCase()}`;
    statusElement.innerHTML = `
            <div class="status-content">
                <strong>${site.url}</strong><br>
                Status: ${site.status}<br>
                Code: ${site.status_code}
            </div>
            <div class="timestamp">
                ${site.timestamp}
            </div>
        `;

    if (existing) {
      statusList.replaceChild(statusElement, existing);
    } else {
      statusList.insertBefore(statusElement, statusList.firstChild);
    }

    while (statusList.children.length > 10) {
      statusList.removeChild(statusList.lastChild);
    }
  });
});

// WebSocket Disconnection Handling
socket.on("disconnect", () => {
  console.warn("❌ Disconnected from WebSocket server. Reconnecting...");
});

// Handle Enter Key Press
document.getElementById("site-url").addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    startMonitoring();
  }
});
