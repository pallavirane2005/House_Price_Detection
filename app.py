from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('model.pkl')

neighborhoods = ['CollgCr', 'Veenker', 'Crawfor', 'NoRidge', 'Mitchel', 'Somerst', 'NWAmes', 'OldTown', 'BrkSide', 'Sawyer', 'NridgHt', 'SawyerW', 'IDOTRR', 'MeadowV', 'Edwards', 'Timber', 'Gilbert', 'StoneBr', 'ClearCr', 'NPkVill', 'Blmngtn', 'BrDale', 'SWISU', 'Blueste']
house_styles = ['2Story', '1Story', '1.5Fin', '1.5Unf', 'SFoyer', 'SLvl', '2.5Unf', '2.5Fin']
kitchen_quals = ['Gd', 'TA', 'Ex', 'Fa', 'Po']

ne_map = {n: i for i, n in enumerate(neighborhoods)}
hs_map = {h: i for i, h in enumerate(house_styles)}
kq_map = {k: i for i, k in enumerate(kitchen_quals)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        features = [
            float(data['LotArea']),
            int(data['OverallQual']),
            int(data['OverallCond']),
            int(data['YearBuilt']),
            float(data['GrLivArea']),
            int(data['FullBath']),
            int(data['BedroomAbvGr']),
            int(data['TotRmsAbvGrd']),
            int(data['GarageCars']),
            float(data['TotalBsmtSF']),
            ne_map.get(data['Neighborhood'], 0),
            hs_map.get(data['HouseStyle'], 0),
            kq_map.get(data['KitchenQual'], 1)
        ]
        
        prediction = model.predict([features])[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(prediction, 2),
            'formatted_price': f"${prediction:,.2f}"
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)