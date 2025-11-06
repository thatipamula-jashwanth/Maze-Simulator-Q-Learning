import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.qlearning import qlearning_bp
from dotenv import load_dotenv

load_dotenv()

# Correct path to frontend folder
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

app = Flask(__name__, static_folder=FRONTEND_PATH)
CORS(app)

# Register API blueprint
app.register_blueprint(qlearning_bp, url_prefix="/api")

# Serve frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
