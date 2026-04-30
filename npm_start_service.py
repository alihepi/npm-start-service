import subprocess, sys, os, threading, webbrowser
from PIL import Image, ImageDraw
import pystray

APP_NAME     = "IMS Server"
PROJECT_ROOT = r"C:\Users\Bim2\alihepi\IMS\Inventory-Management-System"

npm_process = None

def build_icon():
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([4, 4, size-4, size-4], radius=12, fill=(30, 90, 200))
    cx = size // 2
    draw.rectangle([cx-10, 14, cx+10, 20], fill=(255,255,255))
    draw.rectangle([cx-4,  20, cx+4,  44], fill=(255,255,255))
    draw.rectangle([cx-10, 44, cx+10, 50], fill=(255,255,255))
    return img

def start_npm():
    global npm_process
    if npm_process and npm_process.poll() is None:
        return
    npm_process = subprocess.Popen("npm start", cwd=PROJECT_ROOT, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

def stop_npm():
    global npm_process
    if npm_process and npm_process.poll() is None:
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(npm_process.pid)], creationflags=subprocess.CREATE_NO_WINDOW)
        npm_process = None

def on_quit(icon, item):
    stop_npm()
    icon.stop()

def main():
    threading.Thread(target=start_npm, daemon=True).start()
    icon = pystray.Icon(
        name=APP_NAME,
        icon=build_icon(),
        title=APP_NAME,
        menu=pystray.Menu(
            pystray.MenuItem("Arayuzu Ac", lambda i, item: webbrowser.open("http://localhost:5173")),
            pystray.MenuItem("Cikis", on_quit),
        )
    )
    icon.run()

if __name__ == "__main__":
    main()
