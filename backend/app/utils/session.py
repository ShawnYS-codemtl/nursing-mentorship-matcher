from flask import request, jsonify


def require_session_id():
    """Extract session ID from X-Session-ID header. Returns (sid, None) or (None, error_response)."""
    sid = request.headers.get('X-Session-ID', '').strip()
    if not sid:
        return None, (jsonify({'error': 'Session ID required'}), 401)
    return sid, None
