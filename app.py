from flask import Flask, request, jsonify
from color_analysis import ColorAnalyzer

app = Flask(__name__)
analyzer = ColorAnalyzer()


@app.route('/color', methods=['POST'])
def color_analysis():
    if request.method == 'POST':
        data = request.json
        if 'image' not in data:
            return "No image URL in the request."
        image_url = data['image']
        analyzed_color = analyzer.analyze_color(image_url)
        return analyzed_color


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
