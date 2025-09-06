# COVID-19 Predictive Modeling and Flask API

## Overview
This project, conducted by eHealth Africa, develops a machine learning model to predict the likelihood of COVID-19 positivity based on patient data from Hocus Pocus town. The dataset includes demographic and symptom features, with `Result` (POSITIVE/NEGATIVE) as the target variable. The project includes data preprocessing, exploratory data analysis (EDA), model training, and a Flask API with a user-friendly HTML interface for real-time predictions. Visualizations provide insights into feature importance and relationships with the outcome.

### Key Features
- **Data Preprocessing**: Cleans and prepares data from `COVID19.xlsx`.
- **EDA**: Generates static (PNG) and interactive (HTML) visualizations.
- **Model Training**: Trains multiple models (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting) with cross-validation.
- **Feature Selection**: Focuses on 11 key features: `Sex`, `Fever`, `Cough`, `Headache`, `Runny nose`, `Difficulty breathing or Dyspnea`, `Fatigue or general weakness`, `Nausea`, `Diarrhea`, `Chest pain`, `Vomiting`.
- **Flask API**: Provides a `/predict` endpoint for probability predictions and a `/health` endpoint for server status.
- **HTML Interface**: User-friendly dropdowns for inputting symptoms and demographics.
- **Deployment**: Instructions for Heroku or VPS (e.g., AWS EC2 with Gunicorn/Nginx).

## Project Structure
```
covid19_prediction/
├── covid19_analysis_part1.py      # Data preprocessing and cleaning
├── covid19_analysis_part2.py      # EDA and visualizations
├── covid19_analysis_part3.py      # Model training and feature importance
├── covid19_app.py                 # Flask API
├── index.html                     # HTML interface for predictions
├── cleaned_covid19_data.csv       # Cleaned dataset
├── covid_rf_selected_model.pkl    # Trained Random Forest model
├── visualizations/                # Output folder for EDA plots
│   ├── result_distribution.png
│   ├── correlation_heatmap.png
│   ├── feature_vs_result_bar.png
│   ├── feature_vs_result_box.png
│   ├── chi2_association.png
│   ├── feature_vs_result_interactive.html
│   ├── chi2_association_interactive.html
├── feature_importance.csv         # Feature importance scores
├── app.log                        # Flask API logs
├── README.md                      # This file
```

## Prerequisites
- Python 3.8+
- Dependencies:
  ```
  flask==2.0.1
  joblib==1.2.0
  pandas==1.5.0
  numpy==1.23.0
  scikit-learn==1.2.2
  matplotlib==3.5.2
  seaborn==0.11.2
  plotly==5.9.0
  statsmodels==0.13.2
  scipy==1.8.1
  gunicorn==20.1.0
  ```
- Optional: Excel file `COVID19.xlsx` for initial data preprocessing.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd covid19_prediction
   ```

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually install:
   ```bash
   pip install flask joblib pandas numpy scikit-learn matplotlib seaborn plotly statsmodels scipy gunicorn
   ```

4. **Prepare Data**:
   - If you have `COVID19.xlsx`, run:
     ```bash
     python covid19_analysis_part1.py
     ```
     This generates `cleaned_covid19_data.csv`.
   - If `cleaned_covid19_data.csv` is already available, skip this step.

5. **Run EDA**:
   ```bash
   python covid19_analysis_part2.py
   ```
   This generates visualizations in the `visualizations` folder.

6. **Train Model**:
   ```bash
   python covid19_analysis_part3.py
   ```
   This trains models, saves `covid_rf_selected_model.pkl`, and generates `feature_importance.csv`.

7. **Run Flask App Locally**:
   - Ensure `templates/index.html` and `covid_rf_selected_model.pkl` are in the project directory.
   - Start the Flask server:
     ```bash
     python covid19_app.py
     ```
   - Access the interface at `http://localhost:5000`.

## Usage
### Web Interface
1. Open `http://localhost:5000` in a browser.
2. Use dropdowns to select values (e.g., Male/Female for Sex, Yes/No for symptoms).
3. Click "Predict" to see the likelihood of a POSITIVE COVID-19 result.

### API
- **Health Check**:
  ```bash
  curl http://localhost:5000/health
  ```
  Example response:
  ```json
  {"status":"healthy","model_loaded":true,"template_exists":true}
  ```

- **Prediction**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"Sex": 1, "Fever": 1, "Cough": 1, "Headache": 0, "Runny nose": 0, "Difficulty breathing or Dyspnea": 1, "Fatigue or general weakness": 1, "Nausea": 0, "Diarrhea": 0, "Chest pain": 0, "Vomiting": 0}' http://localhost:5000/predict
  ```
  Example response:
  ```json
  {"prediction":0.85,"status":"success","message":"Likelihood of COVID-19 positive: 0.85"}
  ```

### Visualizations
- View static plots (PNG) in the `visualizations` folder.
- Open `feature_vs_result_interactive.html` and `chi2_association_interactive.html` in a browser for interactive exploration.

## Deployment
### Option 1: Heroku
1. Install Heroku CLI: [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
2. Create `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```
3. Create `Procfile`:
   ```
   web: gunicorn covid19_app:app
   ```
4. Initialize Git and deploy:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create my-covid19-app
   git push heroku main
   ```
5. Add model file:
   ```bash
   git add -f covid_rf_selected_model.pkl
   git commit -m "Add model"
   git push heroku main
   ```
6. Access at `https://my-covid19-app.herokuapp.com`.

### Option 2: VPS (AWS EC2, DigitalOcean)
1. Launch an Ubuntu 22.04 instance and SSH:
   ```bash
   ssh ubuntu@<vps-ip>
   ```
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx git -y
   ```
3. Clone or copy files:
   ```bash
   git clone <repository-url> covid19_prediction
   cd covid19_prediction
   ```
4. Set up virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Configure Gunicorn service (`/etc/systemd/system/covid19app.service`):
   ```
   [Unit]
   Description=Gunicorn for COVID-19 Flask app
   After=network.target
   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/covid19_prediction
   Environment="PATH=/home/ubuntu/covid19_prediction/venv/bin"
   ExecStart=/home/ubuntu/covid19_prediction/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/covid19_prediction/covid19app.sock covid19_app:app
   [Install]
   WantedBy=multi-user.target
   ```
6. Enable and start Gunicorn:
   ```bash
   sudo systemctl start covid19app
   sudo systemctl enable covid19app
   ```
7. Configure Nginx (`/etc/nginx/sites-available/covid19app`):
   ```
   server {
       listen 80;
       server_name <vps-ip> <your-domain>;
       location / {
           include proxy_params;
           proxy_pass http://unix:/home/ubuntu/covid19_prediction/covid19app.sock;
       }
   }
   ```
8. Enable Nginx site and restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/covid19app /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```
9. Allow HTTP traffic:
   ```bash
   sudo ufw allow 80
   ```
10. Secure with HTTPS using Certbot:
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d <your-domain>
    ```

## Visualizations
The `covid19_analysis_part2.py` script generates:
- **Static Plots** (in `visualizations/`):
  - `result_distribution.png`: Distribution of POSITIVE vs. NEGATIVE cases.
  - `correlation_heatmap.png`: Correlations between features.
  - `feature_vs_result_bar.png`: Feature prevalence by Result.
  - `feature_vs_result_box.png`: Feature distributions by Result.
  - `chi2_association.png`: Chi-squared test results for feature association.
- **Interactive Plots**:
  - `feature_vs_result_interactive.html`: Interactive bar plots.
  - `chi2_association_interactive.html`: Interactive chi-squared results.

## Ethical Considerations
- **Bias**: Mitigated by auditing for fairness in feature importance.
- **Privacy**: Use HTTPS and anonymize data to comply with GDPR/HIPAA.
- **Transparency**: Feature importance plots enhance interpretability.
- **Misuse**: Model is a risk assessment tool, not a diagnostic replacement.
- **Equity**: Designed for accessibility in low-resource areas like Hocus Pocus.
- **Accountability**: Regular updates and monitoring for model drift.

## Troubleshooting
- **Missing Model**: Run `covid19_analysis_part3.py` to generate `covid_rf_selected_model.pkl`.
- **Template Errors**: Ensure `templates/index.html` exists.
- **Feature Mismatches**: Verify feature names in `cleaned_covid19_data.csv`:
  ```python
  import pandas as pd
  print(pd.read_csv('cleaned_covid19_data.csv').columns.tolist())
  ```
- **Logs**: Check `app.log` for Flask errors or deployment logs for Heroku/VPS.

## Future Improvements
- Add a `/eda` route to display visualizations in the Flask app.
- Implement rate limiting with `flask-limiter`.
- Enhance model with additional features or ensemble methods.
- Deploy a dashboard for interactive EDA using Plotly Dash.

## Contributors
- eHealth Africa Data Science Team

## License
MIT License