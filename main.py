# poker/main.py
VERSION = "1.0.0"

from app.routes import app

if __name__ == "__main__":
    print(f"Poker API - Version {VERSION}")
    app.run(debug=True, port=5000, host='0.0.0.0')