import base64
from io import BytesIO
from operator import index
from PIL import Image 
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
import httpx
import numpy as np
from aiohttp import ClientSession

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def homdepage():
    return render_template('index.html')

@app.route('/api/getbase64', methods=['POST', 'GET'])
def gen_user():
    try:
        data = request.get_json()
        img_base64 = data.get("img")

        if img_base64:

            img_data = base64.b64decode(img_base64)
            img = Image.open(BytesIO(img_data))
            img = img.resize((128, 128))
            img_array = np.array(img) / 255.0
            

            if img_array.any():
                processed_data = {"img": img_array.tolist()}

                response = httpx.post('http://localhost:5000/predict/', json=processed_data)

                if response.status_code == 200:
                    return jsonify(response.json())


            return jsonify({"error": "Processed data is empty"})
        else:
            return jsonify({"error": "No 'img' provided in request"})
    except Exception as e:
        return jsonify({"error": str(e)})


 

if __name__ == "__main__":
    app.run(debug=True)
