from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os
import json

app = Flask(__name__)

# Load credentials from environment variable
google_creds = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = service_account.Credentials.from_service_account_info(google_creds)
sheets_service = build("sheets", "v4", credentials=creds)

# Your Google Sheet ID and names
SPREADSHEET_ID = "1za-mLco0atjbG3ycJS-mi392UnnvAJME0mRWXAfo83c"
DATA_RANGE = "Sheet1!A:D"
LOG_SHEET = "Log!A:C"

@app.route("/")
def home():
    return "LambdaBot backend is running."

@app.route("/update", methods=["POST"])
def update_sheet():
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"success": False, "error": "No message received."}), 400

    # Get current sheet data
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=DATA_RANGE).execute()
    rows = result.get("values", [])

    updated = False
    for i, row in enumerate(rows):
        name = row[0].strip().lower() if len(row) > 0 else ""
        if name in message.lower():
            if "paid" in message.lower():
                row_num = i + 1
                update_range = f"Sheet1!C{row_num}"
                sheet.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=update_range,
                    valueInputOption="RAW",
                    body={"values": [["$0"]]}
                ).execute()
                log_entry = [datetime.now().isoformat(), name.title(), message]
                sheet.values().append(
                    spreadsheetId=SPREADSHEET_ID,
                    range=LOG_SHEET,
                    valueInputOption="USER_ENTERED",
                    body={"values": [log_entry]}
                ).execute()
                updated = True
                return jsonify({"success": True, "message": f"✅ Updated {name.title()}'s balance and logged it."})

    return jsonify({"success": False, "message": "❌ Could not find member or understand the message."})
