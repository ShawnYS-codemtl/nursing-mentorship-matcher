from flask import Blueprint, request, jsonify
from app.services.importing.import_service import import_data
# from app.services.data_sources.google_sheets import GoogleSheetsDataSource
from app.services.data_sources.csv_source import CSVDataSource
from app.services.importing.mapping import detect_mapping
from app.services.importing.aliases import MENTEE_ALIASES, MENTOR_ALIASES
import csv
import traceback
import io

import_bp = Blueprint("import", __name__)

@import_bp.route("/import", methods=["POST"])
def import_endpoint():
    try:
        mentor_file = request.files.get("mentor_file")
        mentee_file = request.files.get("mentee_file")

        if mentor_file and mentee_file: 

            mentor_text = io.TextIOWrapper(
                mentor_file.stream,
                encoding="utf-8"
            )

            mentee_text = io.TextIOWrapper(
                mentee_file.stream,
                encoding="utf-8"
            )

            mentor_rows = list(csv.DictReader(mentor_text))
            mentee_rows = list(csv.DictReader(mentee_text))

            # Wrap into lambdas to match interface
            result = import_data(
                lambda: mentor_rows,
                lambda: mentee_rows
            )

        else: # send error or maybe backup data
            return jsonify({"error": "CSV files required"}), 400
            # data_source = CSVDataSource('app/data/mentors.csv', 'app/data/mentees.csv')
            # result = import_data(data_source.get_mentor_rows, data_source.get_mentee_rows)

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as e:
        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500

@import_bp.route("/import/preview", methods=["POST"])
def preview_import():

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
