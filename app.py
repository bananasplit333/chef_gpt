from flask import Flask, request, jsonify
from utils import kickoff 
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "ingredient hello"

@app.route('/parse_url', methods=['GET'])
def result():
    print("GET")
    try:
        url = request.args.get('url')
        print(f'URL: {url}')
        result = kickoff(url)

        if result:
            ingredients = result['ingredients']
            instructions = result['cooking_instructions']

            if not ingredients and not instructions:
                return jsonify({"error": "No recipe data found"}), 404
            else:
                return result
        else:
            return jsonify({"error": "Error processing link"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)