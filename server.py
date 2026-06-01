from flask import Flask, jsonify, request, send_from_directory
import subprocess
import json
import os

  # 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')

app = Flask(__name__, static_folder=PUBLIC_DIR, static_url_path='/')

@app.route('/')
def index():
      return send_from_directory(PUBLIC_DIR, 'index.html')

@app.route('/api/a-shares')
def a_shares():
      symbols = request.args.get('symbols', '600519,300750')
      try:
          result = subprocess.run(
              ['python', os.path.join('scripts', 'a-share-fetcher.py'), symbols],
              capture_output=True, text=True, timeout=30
          )
          return jsonify(json.loads(result.stdout))
      except Exception as e:
          return jsonify({"error": f"Error fetching A-share data: {str(e)}"}), 500

@app.route('/api/us-stocks')
def us_stocks():
      symbols = request.args.get('symbols', 'AAPL,TSLA')
      try:
          result = subprocess.run(
              ['python', os.path.join('scripts', 'us-stock-fetcher.py'), symbols],
              capture_output=True, text=True, timeout=30
          )
          return jsonify(json.loads(result.stdout))
      except Exception as e:
          return jsonify({"error": f"Error fetching US stock data: {str(e)}"}), 500

if __name__ == '__main__':
      print("Starting server at http://localhost:3000")
      print("Press CTRL+C to stop the server")
      app.run(host='127.0.0.1', port=3000, debug=False)