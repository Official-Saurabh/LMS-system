from app import app
import webbrowser
import threading 
import time
def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    time.sleep(2)
    threading.Thread(target=open_browser).start()
    app.run(debug=False, host="0.0.0.0", port=5000)
