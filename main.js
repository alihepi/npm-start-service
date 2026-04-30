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

app.on("window-all-closed", () => {});

app.whenReady().then(() => {
  app.setAppUserModelId("IMS Server");

  startNpm();

  tray = new Tray(path.join(__dirname, "icon.png"));
  tray.setToolTip("IMS Server");

  const menu = Menu.buildFromTemplate([
    { label: "Arayuzu Ac", click: () => { require("child_process").exec("start http://localhost:5173"); } },
    { label: "API Ac",     click: () => { require("child_process").exec("start http://localhost:3000"); } },
    { type: "separator" },
    { label: "Yeniden Baslat", click: () => { stopNpm(); setTimeout(startNpm, 1000); } },
    { type: "separator" },
    { label: "Cikis", click: () => { stopNpm(); app.quit(); } },
  ]);

  tray.setContextMenu(menu);
});