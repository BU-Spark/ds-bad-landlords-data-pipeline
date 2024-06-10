from flask import Flask, jsonify

from src.database.database import get_db_connection

app = Flask(__name__)

@app.route('/summary', methods=['GET'])
def get_summary(): 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM processing_summary_table ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        data = dict(row) if row else {}
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
