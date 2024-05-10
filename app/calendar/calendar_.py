from flask  import Blueprint, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
import json
import os

load_dotenv()

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar')
def calendar():
    return render_template(os.getenv('calendar'))

@calendar_bp.route('/events.json')
def events_json():
    return send_from_directory('data', os.getenv('eventos'))

@calendar_bp.route('/save_events', methods=['POST'])
def save_events():
    try:
        data = request.json
        with open(send_from_directory('data', os.getenv('eventos')), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
        return jsonify({'message': 'Events saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# from flask import Blueprint, render_template, request, jsonify, send_from_directory
# import json

# calendar_bp = Blueprint('calendar', __name__)

# @calendar_bp.route('/calendar')
# def calendar():
#     return render_template('calendar.html')

# @calendar_bp.route('/events.json')
# def events_json():
#     return send_from_directory('data', 'events.json')

# @calendar_bp.route('/save_events', methods=['POST'])
# def save_events():
#     try:
#         data = request.json
#         with open('data/events.json', 'w', encoding='utf-8') as json_file:
#             json.dump(data, json_file, indent=2)
#         return jsonify({'message': 'Events saved successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
