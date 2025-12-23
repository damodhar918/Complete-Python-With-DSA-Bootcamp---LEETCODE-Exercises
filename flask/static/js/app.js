// Global state
let uploadedData = null;
let trainedModel = null;
let featureChart = null;

// Tab switching
function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// ==================== FILE UPLOAD ====================
document.addEventListener('DOMContentLoaded', function() {
    setupUploadArea();
    setupBatchUploadArea();
});

function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // Click to select
    uploadArea.addEventListener('click', () => fileInput.click());

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            uploadFile();
        }
    });

    fileInput.addEventListener('change', uploadFile);
}

function setupBatchUploadArea() {
    const uploadArea = document.getElementById('batchUploadArea');
    const fileInput = document.getElementById('batchFileInput');

    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
        }
    });
}

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const statusDiv = document.getElementById('uploadStatus');

    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    showStatus(statusDiv, 'Uploading file...', 'loading');

    try {
        const response = await axios.post('/upload', formData);
        uploadedData = response.data;

        showStatus(statusDiv, 'File uploaded successfully!', 'success');
        displayFilePreview(response.data);
        updateAvailableColumns();

    } catch (error) {
        showStatus(statusDiv, 'Error uploading file: ' + error.response.data.error, 'error');
    }
}

function displayFilePreview(data) {
    const preview = document.getElementById('filePreview');
    
    document.getElementById('previewFilename').textContent = data.filename;
    document.getElementById('previewShape').textContent = `${data.shape[0]} rows × ${data.shape[1]} cols`;
    document.getElementById('previewRows').textContent = data.rows;
    document.getElementById('previewCols').textContent = data.columns.length;

    // Data types
    const dtypesList = document.getElementById('dtypesList');
    dtypesList.innerHTML = '';
    Object.entries(data.dtypes).forEach(([col, type]) => {
        const item = document.createElement('div');
        item.className = 'type-item';
        item.innerHTML = `<strong>${col}</strong>: ${type}`;
        dtypesList.appendChild(item);
    });

    // Null counts
    const nullList = document.getElementById('nullList');
    nullList.innerHTML = '';
    Object.entries(data.null_counts).forEach(([col, count]) => {
        if (count > 0) {
            const item = document.createElement('div');
            item.className = 'null-item';
            item.innerHTML = `<strong>${col}</strong>: ${count} missing`;
            nullList.appendChild(item);
        }
    });

    // Data sample
    document.getElementById('dataSample').innerHTML = data.head;
    
    // Statistics
    document.getElementById('statistics').innerHTML = data.statistics;

    preview.style.display = 'block';
}

function updateAvailableColumns() {
    if (!uploadedData) return;

    const columns = uploadedData.columns;

    // Update target column select
    const targetSelect = document.getElementById('targetColumn');
    targetSelect.innerHTML = '';
    columns.forEach(col => {
        const option = document.createElement('option');
        option.value = col;
        option.textContent = col;
        targetSelect.appendChild(option);
    });

    // Update features checkboxes
    const featuresList = document.getElementById('featuresList');
    featuresList.innerHTML = '';
    columns.forEach(col => {
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = col;
        checkbox.checked = true;
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(col));
        featuresList.appendChild(label);
    });

    updateTargetOptions();
}

function updateTargetOptions() {
    // Ensure target and features are different
    const targetSelect = document.getElementById('targetColumn');
    const checkboxes = document.querySelectorAll('#featuresList input[type="checkbox"]');

    checkboxes.forEach(checkbox => {
        checkbox.disabled = checkbox.value === targetSelect.value;
    });
}

// ==================== DATA ANALYSIS ====================
async function analyzeData() {
    if (!uploadedData) {
        showAlert('Please upload a file first');
        return;
    }

    const resultDiv = document.getElementById('analysisResults');
    showStatus(resultDiv, 'Analyzing data...', 'loading');

    try {
        const response = await axios.post('/analyze');
        const data = response.data;

        let html = '<div class="info-grid">';
        html += `<div class="info-item"><strong>Shape</strong><br><span>${data.shape[0]} × ${data.shape[1]}</span></div>`;
        html += `<div class="info-item"><strong>Numeric Columns</strong><br><span>${data.numeric_cols.length}</span></div>`;
        html += `<div class="info-item"><strong>Categorical Columns</strong><br><span>${data.categorical_cols.length}</span></div>`;
        html += '</div>';

        // Missing values summary
        html += '<h4>Missing Values Summary</h4>';
        html += '<div class="info-grid">';
        Object.entries(data.null_percentage).forEach(([col, pct]) => {
            if (pct > 0) {
                html += `<div class="info-item"><strong>${col}</strong><br><span>${pct}% missing</span></div>`;
            }
        });
        html += '</div>';

        // Numeric columns stats
        if (data.numeric_cols.length > 0) {
            html += '<h4>Numeric Columns</h4>';
            html += '<div class="info-grid">';
            data.numeric_cols.forEach(col => {
                html += `<div class="info-item"><strong>${col}</strong></div>`;
            });
            html += '</div>';
        }

        // Categorical columns
        if (data.categorical_cols.length > 0) {
            html += '<h4>Categorical Columns</h4>';
            html += '<div class="info-grid">';
            data.categorical_cols.forEach(col => {
                html += `<div class="info-item"><strong>${col}</strong></div>`;
            });
            html += '</div>';
        }

        resultDiv.innerHTML = html;
        resultDiv.classList.remove('status', 'loading');
        resultDiv.style.display = 'block';

    } catch (error) {
        showStatus(resultDiv, 'Error analyzing data: ' + (error.response?.data?.error || error.message), 'error');
    }
}

// ==================== MODEL TRAINING ====================
async function trainModel() {
    if (!uploadedData) {
        showAlert('Please upload a file first');
        return;
    }

    const modelType = document.getElementById('modelType').value;
    const targetColumn = document.getElementById('targetColumn').value;
    const testSize = document.getElementById('testSize').value / 100;

    // Get selected features
    const featureCheckboxes = document.querySelectorAll('#featuresList input[type="checkbox"]:checked');
    const featureColumns = Array.from(featureCheckboxes).map(cb => cb.value);

    if (featureColumns.length === 0) {
        showAlert('Please select at least one feature');
        return;
    }

    const statusDiv = document.getElementById('trainingStatus');
    showStatus(statusDiv, 'Training model...', 'loading');

    const endpoint = modelType === 'regression' ? '/train-regression' : '/train-classification';

    try {
        const response = await axios.post(endpoint, {
            target_column: targetColumn,
            feature_columns: featureColumns,
            test_size: testSize
        });

        trainedModel = response.data;
        showStatus(statusDiv, 'Model trained successfully!', 'success');
        displayTrainingResults(response.data, featureColumns);

    } catch (error) {
        showStatus(statusDiv, 'Error training model: ' + (error.response?.data?.error || error.message), 'error');
    }
}

function displayTrainingResults(data, featureColumns) {
    const resultsDiv = document.getElementById('trainingResults');
    const metricsDiv = document.getElementById('performanceMetrics');

    let metricsHTML = '';

    if (data.train_r2 !== undefined) {
        // Regression metrics
        metricsHTML += `
            <div class="metric-card">
                <div class="label">Train R² Score</div>
                <div class="value">${data.train_r2.toFixed(4)}</div>
            </div>
            <div class="metric-card">
                <div class="label">Test R² Score</div>
                <div class="value">${data.test_r2.toFixed(4)}</div>
            </div>
            <div class="metric-card">
                <div class="label">Train RMSE</div>
                <div class="value">${data.train_rmse.toFixed(4)}</div>
            </div>
            <div class="metric-card">
                <div class="label">Test RMSE</div>
                <div class="value">${data.test_rmse.toFixed(4)}</div>
            </div>
        `;
    } else {
        // Classification metrics
        metricsHTML += `
            <div class="metric-card">
                <div class="label">Train Accuracy</div>
                <div class="value">${(data.train_accuracy * 100).toFixed(2)}%</div>
            </div>
            <div class="metric-card">
                <div class="label">Test Accuracy</div>
                <div class="value">${(data.test_accuracy * 100).toFixed(2)}%</div>
            </div>
        `;
    }

    metricsDiv.innerHTML = metricsHTML;

    // Feature importance chart
    displayFeatureImportance(data.feature_importance);

    // Predictions sample
    const predTableBody = document.getElementById('predictionsSample');
    predTableBody.innerHTML = '';
    for (let i = 0; i < data.samples; i++) {
        const row = `
            <tr>
                <td>${data.actual[i]}</td>
                <td>${data.predicted[i]}</td>
            </tr>
        `;
        predTableBody.innerHTML += row;
    }

    resultsDiv.style.display = 'block';
}

function displayFeatureImportance(importance) {
    const ctx = document.getElementById('featureChart').getContext('2d');
    
    const labels = Object.keys(importance);
    const values = Object.values(importance);

    if (featureChart) {
        featureChart.destroy();
    }

    featureChart = new Chart(ctx, {
        type: 'barHorizontal',
        data: {
            labels: labels,
            datasets: [{
                label: 'Feature Importance',
                data: values,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: Math.max(...values) * 1.1
                }
            }
        }
    });
}

// ==================== PREDICTIONS ====================
async function predictSingle() {
    if (!trainedModel) {
        showAlert('Please train a model first');
        return;
    }

    const form = document.getElementById('singlePredictForm');
    const inputs = form.querySelectorAll('input, select');
    const inputData = {};

    inputs.forEach(input => {
        inputData[input.name] = parseFloat(input.value) || input.value;
    });

    const resultDiv = document.getElementById('singlePredictResult');
    resultDiv.innerHTML = '<div class="spinner"></div>';
    resultDiv.classList.add('show');

    try {
        const response = await axios.post('/predict', { data: inputData });
        displayPredictionResult(response.data, resultDiv);

    } catch (error) {
        resultDiv.classList.add('error');
        resultDiv.innerHTML = `<p><strong>Error:</strong> ${error.response?.data?.error || error.message}</p>`;
    }
}

function displayPredictionResult(data, resultDiv) {
    let html = '<h3>Prediction Result</h3>';

    if (data.model_type === 'regression') {
        html += `
            <div class="result-value">${data.prediction.toFixed(4)}</div>
            <p><strong>Model Type:</strong> Regression</p>
        `;
    } else {
        html += `
            <div class="result-value">${data.prediction}</div>
            <p><strong>Model Type:</strong> Classification</p>
        `;

        if (data.probability) {
            html += '<h4>Class Probabilities</h4>';
            html += '<ul class="probability-list">';
            data.probability.forEach((prob, idx) => {
                html += `
                    <li class="probability-item">
                        <span>Class ${idx}: ${(prob * 100).toFixed(2)}%</span>
                        <div class="probability-bar" style="width: ${prob * 100}%"></div>
                    </li>
                `;
            });
            html += '</ul>';
        }
    }

    resultDiv.innerHTML = html;
    resultDiv.classList.remove('error');
    resultDiv.classList.add('success');
}

async function predictBatch() {
    if (!trainedModel) {
        showAlert('Please train a model first');
        return;
    }

    const fileInput = document.getElementById('batchFileInput');
    const file = fileInput.files[0];

    if (!file) {
        showAlert('Please select a file for batch prediction');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const resultDiv = document.getElementById('batchPredictResult');
    resultDiv.innerHTML = '<div class="spinner"></div>';
    resultDiv.classList.add('show');

    try {
        const response = await axios.post('/batch-predict', formData);

        let html = `
            <h3>Batch Prediction Results</h3>
            <p><strong>Predictions Made:</strong> ${response.data.count}</p>
            <a href="javascript:void(0)" onclick="downloadBatchResults('${response.data.csv}')" class="btn btn-primary">
                📥 Download Predictions CSV
            </a>
        `;

        resultDiv.innerHTML = html;
        resultDiv.classList.add('success');

    } catch (error) {
        resultDiv.classList.add('error');
        resultDiv.innerHTML = `<p><strong>Error:</strong> ${error.response?.data?.error || error.message}</p>`;
    }
}

function downloadBatchResults(csv) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'predictions.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// ==================== UTILITY FUNCTIONS ====================
function showStatus(element, message, type) {
    element.className = `status show ${type}`;
    element.textContent = message;
}

function showAlert(message) {
    alert(message);
}

// Setup form for single prediction
document.addEventListener('DOMContentLoaded', function() {
    // After model training, update the prediction form
    const originalTrainModel = window.trainModel;
    window.trainModel = async function() {
        await originalTrainModel();
        if (trainedModel) {
            updatePredictionForm();
        }
    };
});

function updatePredictionForm() {
    if (!uploadedData) return;

    const form = document.getElementById('singlePredictForm');
    form.innerHTML = '';

    uploadedData.columns.forEach(col => {
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';

        const label = document.createElement('label');
        label.htmlFor = `input-${col}`;
        label.textContent = col;

        const input = document.createElement('input');
        input.id = `input-${col}`;
        input.name = col;
        input.type = 'number';
        input.placeholder = `Enter ${col}`;
        input.step = 'any';

        formGroup.appendChild(label);
        formGroup.appendChild(input);
        form.appendChild(formGroup);
    });
}
