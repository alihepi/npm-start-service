import subprocess, sys, os, threading, webbrowser
from PIL import Image, ImageDraw
import pystray

APP_NAME      = "IMS Server"
FRONTEND_URL  = "http://localhost:5173"
BACKEND_URL   = "http://localhost:3000"
ICON_COLOR_BG = (30, 90, 200)
ICON_COLOR_FG = (255, 255, 255)
PROJECT_ROOT  = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))

npm_process = None

def build_icon():
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([4, 4, size-4, size-4], radius=12, fill=ICON_COLOR_BG)
    cx = size // 2
    draw.rectangle([cx-10, 14, cx+10, 20], fill=ICON_COLOR_FG)
    draw.rectangle([cx-4,  20, cx+4,  44], fill=ICON_COLOR_FG)
    draw.rectangle([cx-10, 44, cx+10, 50], fill=ICON_COLOR_FG)
    return img

def start_npm():
    global npm_process
    if npm_process and npm_process.poll() is None:
        return
    kwargs = dict(cwd=PROJECT_ROOT, shell=True)
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    npm_process = subprocess.Popen("npm start", **kwargs)

def stop_npm():
    global npm_process
    if npm_process and npm_process.poll() is None:
        if sys.platform == "win32":
            subprocess.call(["taskkill", "/F", "/T", "/PID", str(npm_process.pid)], creationflags=subprocess.CREATE_NO_WINDOW)
        npm_process = None

def get_status_label(): return "Calisiyor" if npm_process and npm_process.poll() is None else "Durduruldu"
def on_open_frontend(icon, item): webbrowser.open(FRONTEND_URL)
def on_open_backend(icon, item): webbrowser.open(BACKEND_URL)
def on_restart(icon, item):
    stop_npm()
    threading.Thread(target=start_npm, daemon=True).start()
def on_quit(icon, item):
    stop_npm()
    icon.stop()

def build_menu():
    return pystray.Menu(
        pystray.MenuItem(lambda _: get_status_label(), None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Arayuzu Ac (Frontend)", on_open_frontend),
        pystray.MenuItem("API Ac (Backend)",      on_open_backend),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Yeniden Baslat",        on_restart),
        pystray.MenuItem("Cikis",                 on_quit),
    )

def main():
    threading.Thread(target=start_npm, daemon=True).start()
    icon = pystray.Icon(name=APP_NAME, icon=build_icon(), title=APP_NAME, menu=build_menu())
    icon.run()

if __name__ == "__main__":
    main()
