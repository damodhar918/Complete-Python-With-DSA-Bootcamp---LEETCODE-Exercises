from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import json
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables to store data and models
current_data = None
current_model = None
model_type = None
feature_columns = None
target_column = None

@app.route('/')
def index():
    """Main page"""
    return render_template('predict_index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload"""
    global current_data
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400
        
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode('utf-8'), newline=None)
        current_data = pd.read_csv(stream)
        
        # Prepare response data
        response = {
            'filename': file.filename,
            'rows': len(current_data),
            'columns': list(current_data.columns),
            'shape': list(current_data.shape),
            'head': current_data.head(10).to_html(),
            'dtypes': current_data.dtypes.astype(str).to_dict(),
            'null_counts': current_data.isnull().sum().to_dict(),
            'statistics': current_data.describe().to_html()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_data():
    """Analyze uploaded data"""
    global current_data
    
    try:
        if current_data is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        analysis = {
            'shape': list(current_data.shape),
            'columns': list(current_data.columns),
            'dtypes': current_data.dtypes.astype(str).to_dict(),
            'null_counts': current_data.isnull().sum().to_dict(),
            'null_percentage': (current_data.isnull().sum() / len(current_data) * 100).round(2).to_dict(),
            'numeric_cols': list(current_data.select_dtypes(include=[np.number]).columns),
            'categorical_cols': list(current_data.select_dtypes(include=['object']).columns),
            'correlation': current_data.corr().to_json() if len(current_data.select_dtypes(include=[np.number]).columns) > 0 else {},
            'statistics': current_data.describe().to_json()
        }
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train-regression', methods=['POST'])
def train_regression():
    """Train regression model"""
    global current_data, current_model, model_type, feature_columns, target_column
    
    try:
        if current_data is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        data = request.json
        target = data.get('target_column')
        features = data.get('feature_columns', [])
        test_size = float(data.get('test_size', 0.2))
        
        if not target or not features:
            return jsonify({'error': 'Target and feature columns required'}), 400
        
        if target not in current_data.columns:
            return jsonify({'error': f'Target column "{target}" not found'}), 400
        
        # Prepare data
        X = current_data[features].fillna(current_data[features].mean())
        y = current_data[target].fillna(current_data[target].mean())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_pred = model.predict(X_train_scaled)
        test_pred = model.predict(X_test_scaled)
        
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
        
        # Feature importance
        feature_importance = dict(zip(features, model.feature_importances_.tolist()))
        feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        
        # Store model
        current_model = {'model': model, 'scaler': scaler}
        model_type = 'regression'
        feature_columns = features
        target_column = target
        
        return jsonify({
            'status': 'success',
            'train_r2': round(train_r2, 4),
            'test_r2': round(test_r2, 4),
            'train_rmse': round(train_rmse, 4),
            'test_rmse': round(test_rmse, 4),
            'feature_importance': feature_importance,
            'samples': min(10, len(test_pred)),
            'actual': y_test.head(10).values.tolist(),
            'predicted': test_pred[:10].tolist()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train-classification', methods=['POST'])
def train_classification():
    """Train classification model"""
    global current_data, current_model, model_type, feature_columns, target_column
    
    try:
        if current_data is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        data = request.json
        target = data.get('target_column')
        features = data.get('feature_columns', [])
        test_size = float(data.get('test_size', 0.2))
        
        if not target or not features:
            return jsonify({'error': 'Target and feature columns required'}), 400
        
        if target not in current_data.columns:
            return jsonify({'error': f'Target column "{target}" not found'}), 400
        
        # Prepare data
        X = current_data[features].fillna(current_data[features].mean())
        y = current_data[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_pred = model.predict(X_train_scaled)
        test_pred = model.predict(X_test_scaled)
        
        train_acc = accuracy_score(y_train, train_pred)
        test_acc = accuracy_score(y_test, test_pred)
        
        # Feature importance
        feature_importance = dict(zip(features, model.feature_importances_.tolist()))
        feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        
        # Classification report
        class_report = classification_report(y_test, test_pred, output_dict=True)
        
        # Store model
        current_model = {'model': model, 'scaler': scaler}
        model_type = 'classification'
        feature_columns = features
        target_column = target
        
        return jsonify({
            'status': 'success',
            'train_accuracy': round(train_acc, 4),
            'test_accuracy': round(test_acc, 4),
            'feature_importance': feature_importance,
            'classification_report': class_report,
            'classes': list(model.classes_),
            'samples': min(10, len(test_pred)),
            'actual': y_test.head(10).astype(str).values.tolist(),
            'predicted': test_pred[:10].astype(str).tolist()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Make predictions on new data"""
    try:
        if current_model is None:
            return jsonify({'error': 'No trained model available'}), 400
        
        data = request.json
        input_data = data.get('data', {})
        
        # Prepare input
        df_input = pd.DataFrame([input_data])
        X_input = df_input[feature_columns].fillna(0)
        X_scaled = current_model['scaler'].transform(X_input)
        
        # Make prediction
        model = current_model['model']
        if model_type == 'regression':
            prediction = model.predict(X_scaled)[0]
            probability = None
        else:
            prediction = model.predict(X_scaled)[0]
            probability = model.predict_proba(X_scaled)[0].tolist()
        
        return jsonify({
            'prediction': float(prediction),
            'probability': probability,
            'model_type': model_type
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Batch predictions"""
    try:
        if current_model is None:
            return jsonify({'error': 'No trained model available'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        stream = io.StringIO(file.stream.read().decode('utf-8'), newline=None)
        df_batch = pd.read_csv(stream)
        
        # Prepare data
        X_batch = df_batch[feature_columns].fillna(0)
        X_scaled = current_model['scaler'].transform(X_batch)
        
        # Make predictions
        model = current_model['model']
        predictions = model.predict(X_scaled)
        
        # Add predictions to dataframe
        df_batch['prediction'] = predictions
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        df_batch.to_csv(csv_buffer, index=False)
        
        return jsonify({
            'status': 'success',
            'predictions': predictions.tolist(),
            'count': len(predictions),
            'csv': csv_buffer.getvalue()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data-summary', methods=['GET'])
def data_summary():
    """Get current data summary"""
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data loaded'}), 400
    
    return jsonify({
        'shape': list(current_data.shape),
        'columns': list(current_data.columns),
        'numeric_cols': list(current_data.select_dtypes(include=[np.number]).columns),
        'categorical_cols': list(current_data.select_dtypes(include=['object']).columns)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
