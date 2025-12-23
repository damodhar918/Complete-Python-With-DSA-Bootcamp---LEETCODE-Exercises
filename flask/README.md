# CSV Data Prediction & Analysis Application

A comprehensive web application for data analysis and machine learning predictions using Flask, Jinja, scikit-learn, and JavaScript.

## Features

### 📊 Data Upload & Preview
- Upload CSV files with drag-and-drop support
- View data summary, statistics, and data types
- Identify missing values
- Preview first 10 rows of data

### 📈 Data Analysis
- Statistical analysis of numeric columns
- Identify numeric and categorical columns
- Calculate missing value percentages
- View correlation statistics

### 🤖 Machine Learning Models
- **Regression Models**: Predict continuous values using Random Forest
- **Classification Models**: Predict classes using Random Forest Classifier
- Training/test split configuration
- Feature selection
- Model performance metrics (R², RMSE, Accuracy)
- Feature importance visualization

### 🔮 Predictions
- **Single Prediction**: Input values and get instant predictions
- **Batch Predictions**: Upload CSV file for multiple predictions
- Download prediction results as CSV

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **ML Library**: scikit-learn (Random Forest models)
- **Data Processing**: pandas, numpy
- **Visualization**: Chart.js
- **HTTP Client**: Axios

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**
```bash
cd c:\Users\jdamodhar\Downloads\flask
```

2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install required packages**
```bash
pip install flask pandas numpy scikit-learn werkzeug
```

4. **Run the application**
```bash
python predict_app.py
```

5. **Open in browser**
- Navigate to: `http://localhost:5000`

## Project Structure

```
flask/
├── predict_app.py                 # Main Flask application
├── sample_data.csv               # Sample CSV file for testing
├── templates/
│   └── predict_index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── predict_style.css     # Styling
│   └── js/
│       └── app.js                # Frontend JavaScript
└── uploads/                       # Uploaded files directory
```

## Usage Guide

### Step 1: Upload Data
1. Click the **Upload** tab
2. Drag and drop a CSV file or click to select
3. View file preview, statistics, and data types

### Step 2: Analyze Data
1. Switch to **Analysis** tab
2. Click "Analyze Data" button
3. View statistics, missing values, and column information

### Step 3: Train Model
1. Go to **Train Model** tab
2. Choose model type:
   - **Regression**: For continuous value prediction (e.g., salary, price)
   - **Classification**: For category prediction (e.g., yes/no, categories)
3. Select target column (what you want to predict)
4. Select feature columns (input variables)
5. Adjust test size (default 20%)
6. Click "Train Model"
7. View performance metrics and feature importance

### Step 4: Make Predictions
1. Switch to **Predict** tab
2. **Single Prediction**: Enter values for each feature and click "Predict"
3. **Batch Prediction**: Upload CSV file with same columns as training data

## Sample CSV Format

Example: `sample_data.csv` (Salary prediction)
```csv
Age,Salary,Years_Experience,Department,Performance_Score,Bonus_Percentage
25,45000,1,Sales,72,5
28,52000,3,Marketing,78,8
...
```

**To train regression model**: Select "Salary" as target, others as features
**To train classification model**: Select "Department" as target

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/upload` | POST | Upload CSV file |
| `/analyze` | POST | Analyze uploaded data |
| `/train-regression` | POST | Train regression model |
| `/train-classification` | POST | Train classification model |
| `/predict` | POST | Make single prediction |
| `/batch-predict` | POST | Make batch predictions |
| `/data-summary` | GET | Get data summary |

## Configuration

### File Size Limit
- Maximum upload size: 50MB
- Configurable in `predict_app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
```

### Model Parameters
- Algorithm: Random Forest
- Number of trees: 100
- Random state: 42 (for reproducibility)
- Scaling: StandardScaler

## Customization

### Change Model Algorithm
Edit `predict_app.py` and replace Random Forest with other sklearn models:
```python
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(...)
```

### Adjust Styling
Edit `static/css/predict_style.css` to customize colors and layout

### Add More Features
Extend `static/js/app.js` for additional functionality

## Error Handling

The application includes error handling for:
- Invalid file formats
- Missing values in data
- Column mismatches
- Model training failures
- Prediction errors

## Performance Tips

1. **Data Preprocessing**: Handle missing values before upload
2. **Feature Selection**: Choose relevant features for better accuracy
3. **Data Scaling**: Application automatically scales numeric features
4. **Batch Size**: For very large batch predictions, split into smaller files

## Troubleshooting

### Port Already in Use
Change port in `predict_app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Missing Dependencies
Ensure all packages are installed:
```bash
pip install -r requirements.txt
```

### File Upload Issues
- Check file is valid CSV format
- Ensure file size < 50MB
- Verify CSV has proper headers

## Future Enhancements

- [ ] Support for more ML algorithms (SVM, Neural Networks)
- [ ] Cross-validation support
- [ ] Hyperparameter tuning interface
- [ ] Model export/import functionality
- [ ] Data visualization (scatter plots, histograms)
- [ ] Advanced feature engineering
- [ ] Database integration
- [ ] User authentication

## License

MIT License

## Author

Created as a comprehensive Flask ML application for CSV data analysis and predictions.

## Support

For issues or questions, please check:
1. Python version compatibility
2. Required packages installation
3. File format and data quality
4. Browser console for JavaScript errors

---

**Happy Predicting!** 🚀
