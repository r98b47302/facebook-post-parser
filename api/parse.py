import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/parse')
def parse():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        og_desc = soup.find('meta', property='og:description')
        og_title = soup.find('meta', property='og:title')

        return jsonify({
            "url": url,
            "title": og_title['content'] if og_title else None,
            "description": og_desc['content'] if og_desc else None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
