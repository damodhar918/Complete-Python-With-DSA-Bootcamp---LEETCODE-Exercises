# Quick Start Guide - CSV Prediction App

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python predict_app.py
```

### Step 3: Open Browser
Navigate to: **http://localhost:5000**

---

## 📚 Example Walkthrough

### Using Sample Data (sample_data.csv)

**Dataset**: Employee Salary Data
- **Rows**: 20 employees
- **Features**: Age, Years_Experience, Performance_Score, Bonus_Percentage, Department
- **Target**: Salary (for regression)

### Regression Example (Predict Salary)

1. **Upload**: Click upload area → Select `sample_data.csv`
2. **Analysis**: Check data statistics and correlations
3. **Train Model**:
   - Model Type: **Regression**
   - Target Column: **Salary**
   - Features: Age, Years_Experience, Performance_Score, Bonus_Percentage ✓
   - Click **Train Model**
4. **Predict**:
   - Input: Age=35, Years_Experience=10, Performance_Score=85, Bonus_Percentage=12
   - Click **Predict** → Get predicted salary!

### Classification Example (Predict Department)

1. **Upload**: Same CSV file
2. **Train Model**:
   - Model Type: **Classification**
   - Target Column: **Department**
   - Features: Age, Salary, Years_Experience, Performance_Score ✓
   - Click **Train Model**
3. **Predict**:
   - Input values for features
   - Get predicted department + probability for each class

---

## 🎯 Key Features Explained

| Feature | What It Does |
|---------|-------------|
| **File Preview** | Shows data types, missing values, statistics |
| **Analyze Data** | Calculates correlations and data quality metrics |
| **Model Type** | Choose between Regression (continuous) or Classification (categories) |
| **Feature Selection** | Pick which columns to use for prediction |
| **Train Model** | Builds ML model from selected data |
| **Feature Importance** | Shows which features matter most |
| **Single Predict** | Predict for one data point |
| **Batch Predict** | Upload CSV and predict for many rows |

---

## 💡 Tips & Tricks

1. **Best Data Size**: 100+ rows for reliable models
2. **Missing Values**: App handles some, but clean data works better
3. **Feature Selection**: More features ≠ better model
4. **Test Size**: Default 20% works well (80% train, 20% test)
5. **Batch Predictions**: Ensure CSV has same columns as training data

---

## 🔧 Customization

### Change Colors
Edit `static/css/predict_style.css`:
```css
--primary-color: #667eea;      /* Change this */
--secondary-color: #764ba2;    /* And this */
```

### Change Port
Edit `predict_app.py`:
```python
app.run(debug=True, port=5001)  # Use 5001 instead of 5000
```

### Change Upload Limit
Edit `predict_app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB instead of 50MB
```

---

## ❓ Common Questions

**Q: Can I use non-numeric data?**
A: Yes! Categorical data (text) is handled automatically for classification.

**Q: What if my CSV has missing values?**
A: The app fills numeric missing values with the column mean.

**Q: How accurate are predictions?**
A: Depends on data quality and relevance of features. Check R² score (regression) or Accuracy (classification).

**Q: Can I export predictions?**
A: Yes! Use "Batch Predict" and click "Download Predictions CSV".

**Q: What machine learning algorithms are used?**
A: Random Forest (100 trees) - great for both regression and classification.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | Change port in `predict_app.py` |
| Module not found error | Run `pip install -r requirements.txt` |
| File upload fails | Ensure file is CSV format with valid headers |
| Model training fails | Check that target column is different from features |
| No predictions showing | Train a model first before predicting |

---

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│         Browser (Frontend)              │
│  HTML/Jinja + CSS + JavaScript + Chart  │
└────────────┬────────────────────────────┘
             │
        HTTP/AJAX
             │
┌────────────▼────────────────────────────┐
│       Flask Backend (Python)            │
│  - File Upload & Processing             │
│  - Data Analysis                        │
│  - Model Training (sklearn)             │
│  - Predictions                          │
└─────────────────────────────────────────┘
```

---

## 🎓 Learning Outcomes

After using this app, you'll understand:
- How web apps handle file uploads
- Data preprocessing with pandas
- Machine learning with scikit-learn
- Frontend-backend communication with AJAX
- Real-time model training and prediction

---

## 📝 Next Steps

1. Try with your own CSV data
2. Experiment with different features
3. Compare regression vs classification
4. Check feature importance to understand data patterns
5. Modify the code to add custom features!

**Happy Data Science! 🚀📊**
