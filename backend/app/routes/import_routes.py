from flask import Blueprint, request, jsonify
from app.services.importing.import_service import import_data
from app.services.data_sources.csv_source import CSVDataSource
from app.services.importing.mapping import detect_mapping
from app.services.importing.aliases import MENTEE_ALIASES, MENTOR_ALIASES
from app.services.importing.normalization import normalize_rows
from app.services.importing.validation import validate_rows, REQUIRED_MENTEE_FIELDS, REQUIRED_MENTOR_FIELDS
from app.utils.session import require_session_id
import csv
import traceback
import io
import json

import_bp = Blueprint("import", __name__)

@import_bp.route("/import/preview", methods=["POST"])
def preview_import():
    # Preview doesn't persist data, but still require session for consistency
    session_id, err = require_session_id()
    if err:
        return err

    try:
        mentor_file = request.files.get("mentor_file")
        mentee_file = request.files.get("mentee_file")

        if not mentor_file or not mentee_file:
            return jsonify({
                "error": "Both files required"
            }), 400

        mentor_text = io.TextIOWrapper(
            mentor_file.stream,
            encoding="utf-8"
        )

        mentee_text = io.TextIOWrapper(
            mentee_file.stream,
            encoding="utf-8"
        )

        mentor_reader = csv.DictReader(mentor_text)
        mentee_reader = csv.DictReader(mentee_text)

        mentor_headers = mentor_reader.fieldnames or []
        mentee_headers = mentee_reader.fieldnames or []

        mentor_mapping, mentor_unmatched = detect_mapping(
            mentor_headers,
            MENTOR_ALIASES
        )

        mentee_mapping, mentee_unmatched = detect_mapping(
            mentee_headers,
            MENTEE_ALIASES
        )

        return jsonify({
            "mentor": {
                "headers": mentor_headers,
                "mapping": mentor_mapping,
                "unmatched": mentor_unmatched
            },

            "mentee": {
                "headers": mentee_headers,
                "mapping": mentee_mapping,
                "unmatched": mentee_unmatched
            }
        })
    except Exception as e:
        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500

@import_bp.route("/import/confirm", methods=["POST"])
def confirm_import():
    session_id, err = require_session_id()
    if err:
        return err

    try:
        mentor_mapping = json.loads(
            request.form["mentor_mapping"]
        )

        mentee_mapping = json.loads(
            request.form["mentee_mapping"]
        )

        mentor_file = request.files.get("mentor_file")
        mentee_file = request.files.get("mentee_file")

        if not mentor_file or not mentee_file:
            return jsonify({
                "error": "Both CSV files are required"
            }), 400

        mentor_text = io.TextIOWrapper(
            mentor_file.stream,
            encoding="utf-8"
        )

        mentee_text = io.TextIOWrapper(
            mentee_file.stream,
            encoding="utf-8"
        )

        mentor_rows = list(
            csv.DictReader(mentor_text)
        )

        mentee_rows = list(
            csv.DictReader(mentee_text)
        )

        normalized_mentor_rows = normalize_rows(
            mentor_rows,
            mentor_mapping
        )

        normalized_mentee_rows = normalize_rows(
            mentee_rows,
            mentee_mapping
        )

        # =========================
        # Validation
        # =========================

        mentor_errors = validate_rows(
            normalized_mentor_rows,
            REQUIRED_MENTOR_FIELDS
        )

        mentee_errors = validate_rows(
            normalized_mentee_rows,
            REQUIRED_MENTEE_FIELDS
        )

        if mentor_errors or mentee_errors:

            return jsonify({
                "error": "Validation failed",

                "mentor_errors": mentor_errors,
                "mentee_errors": mentee_errors
            }), 400

        # =========================
        # Import
        # =========================

        result = import_data(
            lambda: normalized_mentor_rows,
            lambda: normalized_mentee_rows,
            session_id
        )

        return jsonify({
            "status": "success",
            "data": result,

            "mentor_rows_imported": len(
                normalized_mentor_rows
            ),

            "mentee_rows_imported": len(
                normalized_mentee_rows
            )
        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500
