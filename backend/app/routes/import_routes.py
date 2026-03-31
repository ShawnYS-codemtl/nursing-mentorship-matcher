from flask import Blueprint, request, jsonify
from app.services.importing.import_service import import_data
from app.services.data_sources.google_sheets import GoogleSheetsDataSource
from app.services.data_sources.csv_source import CSVDataSource

import_bp = Blueprint("import", __name__)

@import_bp.route("/import", methods=["POST"])
def import_endpoint():
    try:
        data = request.get_json(silent=True) or {}
        source = (data.get("source") or request.form.get("source") or "").lower()

        print(f"Import source: {source}")

        if source == "google_sheets":
            data_source = GoogleSheetsDataSource()
            result = import_data(data_source.get_mentor_rows, data_source.get_mentee_rows)

        # uploading csv files from frontend
        # fallback to csv files in dev mode
        elif source == "csv":

            mentor_file = request.files.get("mentor_file")
            mentee_file = request.files.get("mentee_file")
            if mentor_file and mentee_file: 

                if not mentor_file or not mentee_file:
                    return jsonify({"error": "CSV files required"}), 400

                import csv

                mentor_rows = list(csv.DictReader(mentor_file.stream))
                mentee_rows = list(csv.DictReader(mentee_file.stream))

                # Wrap into lambdas to match interface
                result = import_data(
                    lambda: mentor_rows,
                    lambda: mentee_rows
                )
            else:
                data_source = CSVDataSource('app/data/mentors.csv', 'app/data/mentees.csv')
                result = import_data(data_source.get_mentor_rows, data_source.get_mentee_rows)

        else:
            return jsonify({"error": "Invalid source"}), 400

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500