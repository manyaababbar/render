from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("\n📥 Webhook received:")
        print(json.dumps(data, indent=2))

        # You can also save it to a file if needed
        with open('last_webhook.json', 'w') as f:
            json.dump(data, f, indent=2)

        return jsonify({"status": "success", "message": "Webhook received"}), 200

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)