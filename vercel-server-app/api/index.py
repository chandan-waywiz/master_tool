import io
import os
import json
import re
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
load_dotenv()
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime, timedelta
from PyPDF2 import PdfMerger
import traceback
from werkzeug.utils import secure_filename
from pymongo import MongoClient, ReturnDocument
import pymongo.errors
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'bmp', 'tiff', 'gif'}
API_KEY = os.environ.get("GEMINI_API_KEY")
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = "id_docs_db"
MONGO_USERS_COLLECTION_NAME = "users"
MONGO_DOCUMENTS_COLLECTION_NAME = "documents"
GEMINI_MODEL_NAME = 'gemini-2.5-flash'
PASSPORT_REDACTION_PLACEHOLDER = "[PASSPORT NUMBER REDACTED]"
AADHAAR_REDACTION_PLACEHOLDER = "[AADHAAR NUMBER REDACTED]"
ID_NUMBER_NOT_FOUND = "NA"
WORD_DOC_TYPE = "word_form"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- MongoDB Setup ---
client = None
db = None
docs_collection = None
users_collection = None
try:
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable not set.")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    docs_collection = db[MONGO_DOCUMENTS_COLLECTION_NAME]
    users_collection = db[MONGO_USERS_COLLECTION_NAME]
    client.admin.command('ping')
except Exception as e:
    client = None

# --- Utility and Route Functions ---
# ...existing code from app.py (functions, routes, etc.)...

# Remove any __main__ block for Vercel compatibility