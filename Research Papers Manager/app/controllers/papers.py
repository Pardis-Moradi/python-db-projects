from flask import Blueprint, request, jsonify

from ..services.papers_service import(
    add_paper, search_for_papers, get_paper_details,
    InvalidUserID, InvalidCitationReference, PaperDoesntExist
)
from ..utils.validators import(
    validate_upload_paper_input, validate_search_papers_parameters
)

papers_bp = Blueprint("papers", __name__)

@papers_bp.route("/papers", methods=["GET", "POST"])
def papers():
    if request.method == "POST":
        return upload_paper(request)
    elif request.method == "GET":
        return search_papers(request)
    
def upload_paper(request):
    user_id = request.headers.get('X-User-ID')
    payload = request.get_json() or {}
    errors  = validate_upload_paper_input(payload)
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        pid = add_paper(user_id, payload)
        return jsonify({
            "message": "Paper uploaded",
            "paper_id": pid
        }), 201
    
    except InvalidUserID:
        return jsonify({"message": "username invalid"}), 401
    
    except InvalidCitationReference:
        return jsonify({"message": "citation reference invalid"}), 404
    
def search_papers(request):
    search_term = request.args.get('search', '').strip()
    sort_by    = request.args.get('sort_by', 'relevance')
    order      = request.args.get('order', 'desc')
    errors = validate_search_papers_parameters(search_term, sort_by, order)
    if errors:
        return jsonify({'errors': errors}), 400
    
    return jsonify({"papers": search_for_papers(search_term, sort_by, order)}), 200

@papers_bp.route("/papers/<paper_id>", methods=["GET"])
def find_paper(paper_id):
    try:
        response = get_paper_details(paper_id)
    except PaperDoesntExist:
        return jsonify({"message": "Paper not found"}), 404
    
    return jsonify(response), 200