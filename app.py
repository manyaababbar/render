from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
import os
from bson import ObjectId

# === Load environment variables from .env file ===
load_dotenv()

# === Flask app setup ===
app = Flask(__name__)
CORS(app)

# === MongoDB Connection using .env ===
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DATABASE_NAME", "workviser")

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db["Employee"]

# === API Route ===
@app.route("/find-employees", methods=["POST"])
def find_employees():
    data = request.get_json()
    domains = data.get("domain")

    if not domains:
        return jsonify({"error": "Missing 'domain'"}), 400

    original_domains = domains if isinstance(domains, list) else [domains]

    result = {}

    for domain in original_domains:
        query = {f"expertise.{domain}": {"$exists": True}}
        employees = collection.find(query)
        
        domain_employees = []
        for emp in employees:
            domain_employees.append({
                "id": str(emp.get("_id")),
                "name": emp.get("name"),
                "work_email": emp.get("work_email"),
                "department": emp.get("department"),
                "position": emp.get("position"),
                "expertise": emp.get("expertise")
            })
        
        result[domain] = domain_employees or None

    # Save to a local file (in project root)
    import json
    with open("employee_result.json", "w", encoding="utf-8") as f:
        json.dump({"employees": result}, f, indent=4)

    return jsonify({"employees": result}), 200


# === Run the app ===
if __name__ == "__main__":
    app.run(debug=True)
