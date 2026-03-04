# 📡 Telco Customer Churn Analysis

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=flat-square&logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Complete-green?style=flat-square)

> End-to-End Machine Learning project for customer churn prediction with an interactive Streamlit dashboard.

---

## 📌 Project Overview

Customer churn is one of the biggest challenges in the telecom industry. This project builds a complete ML pipeline to:

- **Predict** which customers are likely to churn
- **Score** each customer with a Risk Score (0–100)
- **Segment** customers into risk tiers for proactive intervention
- **Visualize** insights through an interactive Streamlit dashboard

---

## 🗂️ Project Structure

```
telco-churn-analysis/
│
├── data/
│   └── telco_churn.csv          # Raw dataset
│
├── output/                      # Generated visualizations & model outputs
│
├── churn.ipynb                  # Main analysis & ML notebook
├── app.py                       # Streamlit dashboard
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🔍 Dataset

- **Source:** Telco Customer Churn Dataset
- **Records:** ~7,000 customers
- **Features:** 21 columns including demographics, services, and billing info
- **Target:** `Churn` (Yes / No)

---

## 🧠 Methodology

### Risk Scoring System
Each customer is evaluated across multiple dimensions:

| Dimension | Features |
|---|---|
| Account characteristics | Contract type, tenure, payment method |
| Service usage patterns | Internet type, add-on services |
| Financial indicators | Monthly charges, payment history |

Each customer receives a **Risk Score (0–100)** enabling proactive intervention.

### Risk Tiers
| Tier | Score Range | Action |
|---|---|---|
| 🔴 Critical | 75–100 | Immediate intervention |
| 🟠 High | 50–74 | Priority outreach |
| 🟡 Medium | 25–49 | Monitor closely |
| 🟢 Low | 0–24 | Retention programs |

---

## 📊 Key Features

- ✅ Exploratory Data Analysis (EDA)
- ✅ Feature Engineering & Preprocessing
- ✅ Risk Score Calculation
- ✅ Customer Segmentation by Risk Tier
- ✅ Confusion Matrix & Model Performance Visualization
- ✅ Interactive Streamlit Dashboard

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Gudurupavankumarreddy/telco-churn-analysis.git
cd telco-churn-analysis
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app
```bash
streamlit run app.py
```

### 5. Open the Jupyter Notebook
```bash
jupyter notebook churn.ipynb
```

---

## 📈 Results

- Risk scoring system successfully segments customers into actionable tiers
- Dashboard enables business teams to identify and prioritize at-risk customers
- Visualizations include Risk Score Distribution and Confusion Matrix

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| Pandas & NumPy | Data manipulation |
| Scikit-Learn | Machine learning |
| Matplotlib & Seaborn | Visualizations |
| Streamlit | Interactive dashboard |
| Jupyter Notebook | Analysis & exploration |

---

## 👤 Author

**Gudurupavankumarreddy**  
📧 GitHub: [@Gudurupavankumarreddy](https://github.com/Gudurupavankumarreddy)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
