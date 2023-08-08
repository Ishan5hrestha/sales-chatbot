from dotenv import load_dotenv
import os
from serpapi import GoogleSearch
import requests
import json
from flask import request, jsonify, Blueprint

from views.openai_view import get_openai_response

load_dotenv()
serpapi_api_key = os.getenv("SERPAPI_P_KEY")

# data_type: TIMESERIES, GEO_MAP, GEO_MAP_0, RELATED_TOPICS, RELATED_QUERIES

# Playground
# https://serpapi.com/playground?engine=google_trends&q=volcano&data_type=RELATED_QUERIES

serpapi_bp = Blueprint('serpapi', __name__)
@serpapi_bp.route('/')
def status():
    return jsonify({"status": "active"})

@serpapi_bp.route('/related_queries', methods=['POST'])
def get_trends():
    try:
        print('here')
        data = request.json
        keywords = data.get("keywords")
        status_type = data.get("status_type")
        print(f"{keywords}, {status_type}")
        
        if not keywords or not status_type:
            return jsonify({"error": "Both 'keywords' and 'status_type' are required."}), 400
        
        related_queries = get_related_queries(keywords, status_type)
        print(related_queries)
        return jsonify({"related_queries": related_queries})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# status_type = rising | top
def get_related_queries(keywords:str, status_type:str):
    params = {
        "engine": "google_trends",
        "q": keywords,
        "data_type": "RELATED_QUERIES",
        "api_key": "f2519cfbe9a6ffed3dd087b4edee2170a8481a92f0092b5a4ccceb818c7e2dd9"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    related_queries = [i["query"] for i in results["related_queries"][status_type]]
    # related_queries = [i["query"] for i in results["related_queries"]["top"]]
    return related_queries
