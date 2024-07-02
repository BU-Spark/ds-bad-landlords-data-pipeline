import sys
import os


# ensures modules can be imported from src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', )))

from flask import Flask, jsonify, request
from database.database import getSQLiteConnection
from criteriaI.processI import getFormattedUniqueBadLandlords
from criteriaIII.processIII import getBadLandlordsFromProblemProperties

app = Flask(__name__)

@app.route('/summary', methods=['GET'])
def getSummary(): 
    try:
        conn = getSQLiteConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM processing_summary_table ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        data = dict(row) if row else {}
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/badlandlords', methods=['GET'])
def getBadLandlords():
    criteria = request.args.get('criteria')
    if criteria not in ['i', 'ii', 'iii', 'all']:
        return jsonify({'error': 'Invalid criteria passed'})
    try:
        rows = None
        if criteria == 'i':
            return getFormattedUniqueBadLandlords()
        if criteria == 'iii':
            return getBadLandlordsFromProblemProperties()
        conn = getSQLiteConnection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM badlandlords_criteria_{criteria}')
        rows = cursor.fetchall()
        conn.close()
        if(rows == None):
            return jsonify([])
        data = [dict(row) for row in rows]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
