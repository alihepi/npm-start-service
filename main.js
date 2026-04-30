const { app, Tray, Menu } = require("electron");
const { exec, execSync } = require("child_process");
const path = require("path");

const PROJECT_ROOT = "C:\\Users\\Bim2\\alihepi\\IMS\\Inventory-Management-System";
let tray = null;
let npmProcess = null;

function startNpm() {
  if (npmProcess) return;
  npmProcess = exec("npm start", { cwd: PROJECT_ROOT, windowsHide: true });
}

function stopNpm() {
  if (!npmProcess) return;
  try { execSync("taskkill /F /T /PID " + npmProcess.pid, { windowsHide: true }); } catch(e) {}
  npmProcess = null;
}

function openUrl(url) {
  exec("start " + url, { windowsHide: true });
}

app.on("ready", () => {
  app.setAppUserModelId("IMS Server");
  startNpm();
  tray = new Tray(path.join(__dirname, "icon.png"));
  tray.setToolTip("IMS Server");
  tray.setContextMenu(Menu.buildFromTemplate([
    { label: "Arayuzu Ac",     click: () => openUrl("http://localhost:5173") },
    { label: "API Ac",         click: () => openUrl("http://localhost:3000") },
    { type: "separator" },
    { label: "Yeniden Baslat", click: () => { stopNpm(); startNpm(); } },
    { label: "Cikis",          click: () => { stopNpm(); app.quit(); } },
  ]));
});

app.dock?.hide();