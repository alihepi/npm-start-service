const { app, Tray, Menu, shell } = require("electron");
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
  try {
    execSync(`taskkill /F /T /PID ${npmProcess.pid}`, { windowsHide: true });
  } catch(e) {}
  npmProcess = null;
}

app.on("window-all-closed", (e) => {
  e.preventDefault();
});

app.whenReady().then(() => {
  app.setAppUserModelId("IMS Server");

  startNpm();

  tray = new Tray(path.join(__dirname, "icon.png"));
  tray.setToolTip("IMS Server - Calisiyor");

  const menu = Menu.buildFromTemplate([
    { label: "Arayuzu Ac", click: () => shell.openExternal("http://localhost:5173") },
    { label: "API Ac",     click: () => shell.openExternal("http://localhost:3000") },
    { type: "separator" },
    { label: "Yeniden Baslat", click: () => { stopNpm(); startNpm(); } },
    { type: "separator" },
    { label: "Cikis", click: () => { stopNpm(); app.quit(); } },
  ]);

  tray.setContextMenu(menu);
});