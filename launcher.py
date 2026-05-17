import sys
import os
import threading
import webbrowser
import time

# Cuando corre como .exe de PyInstaller, los archivos están en sys._MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ['APP_BASE_DIR'] = BASE_DIR

from app import app

PORT = 5000


def _open_browser():
    time.sleep(1.8)
    webbrowser.open(f'http://127.0.0.1:{PORT}')


if __name__ == '__main__':
    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(host='127.0.0.1', port=PORT, debug=False, use_reloader=False, threaded=True)
