"""
Simple Streamlit Dashboard for Telco Churn Analysis
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import joblib

# Page config
st.set_page_config(page_title="Churn Analytics", page_icon="📊", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("output/clean_telco.csv")
    if df['Churn'].dtype == 'object':
        df['Churn'] = df['Churn'].map({'No': 0, 'Yes': 1})
    return df

@st.cache_resource
def load_model():
    try:
        return joblib.load("output/risk_scoring_model.joblib")
    except:
        return None

df = load_data()
model = load_model()

# Sidebar
with st.sidebar:
    st.title("📊 Navigation")
    page = st.radio("", ["Dashboard", "Analysis", "Predictor"])

# Calculate metrics
total = len(df)
churned = (df['Churn'] == 1).sum()
churn_rate = (churned / total) * 100
revenue = df['MonthlyCharges'].sum()

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================
if page == "Dashboard":
    st.title("📊 Telco Churn Analytics Dashboard")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total:,}")
    col2.metric("Churn Rate", f"{churn_rate:.1f}%")
    col3.metric("Churned", f"{churned:,}")
    col4.metric("Monthly Revenue", f"${revenue:,.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Contract analysis
        contract = df.groupby('Contract').agg({'Churn': ['sum', 'count']}).reset_index()
        contract.columns = ['Contract', 'Churned', 'Total']
        contract['Rate'] = (contract['Churned'] / contract['Total']) * 100
        
        fig = px.bar(contract, x='Contract', y='Rate', 
                     text='Rate', title="Churn Rate by Contract (%)")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Churn pie chart
        labels = ['Retained', 'Churned']
        values = [total - churned, churned]
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
        fig.update_layout(title="Customer Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    # Tenure analysis
    st.subheader("📅 Churn by Tenure")
    
    df['Tenure_Group'] = pd.cut(df['tenure'], 
                                 bins=[0, 12, 24, 48, 100],
                                 labels=['0-12mo', '13-24mo', '25-48mo', '48+mo'])
    
    tenure_churn = df.groupby('Tenure_Group', observed=True)['Churn'].agg(['sum', 'count'])
    tenure_churn['Rate'] = (tenure_churn['sum'] / tenure_churn['count']) * 100
    tenure_churn = tenure_churn.reset_index()
    
    fig = px.line(tenure_churn, x='Tenure_Group', y='Rate', 
                  markers=True, title="Churn Rate Across Tenure")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 2: DETAILED ANALYSIS
# ============================================================================
elif page == "Analysis":
    st.title("📈 Detailed Customer Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Service Analysis", "Payment Method", "Demographics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Internet service
            internet = df.groupby('InternetService')['Churn'].agg(['sum', 'count'])
            internet['Rate'] = (internet['sum'] / internet['count']) * 100
            internet = internet.reset_index()
            
            fig = px.bar(internet, x='InternetService', y='Rate',
                        title="Churn by Internet Service")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Tech support
            tech = df.groupby('TechSupport')['Churn'].agg(['sum', 'count'])
            tech['Rate'] = (tech['sum'] / tech['count']) * 100
            tech = tech.reset_index()
            
            fig = px.bar(tech, x='TechSupport', y='Rate',
                        title="Churn by Tech Support")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        payment = df.groupby('PaymentMethod')['Churn'].agg(['sum', 'count'])
        payment['Rate'] = (payment['sum'] / payment['count']) * 100
        payment = payment.reset_index().sort_values('Rate', ascending=False)
        
        fig = px.bar(payment, x='PaymentMethod', y='Rate',
                    title="Churn by Payment Method")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Senior citizen
            senior = df.groupby('SeniorCitizen')['Churn'].mean() * 100
            st.metric("Senior Citizen Churn", f"{senior[1]:.1f}%")
            st.metric("Non-Senior Churn", f"{senior[0]:.1f}%")
        
        with col2:
            # Partner
            partner = df.groupby('Partner')['Churn'].mean() * 100
            st.metric("With Partner Churn", f"{partner['Yes']:.1f}%")
            st.metric("No Partner Churn", f"{partner['No']:.1f}%")

# ============================================================================
# PAGE 3: RISK PREDICTOR
# ============================================================================
elif page == "Predictor":
    st.title("🎯 Customer Churn Risk Predictor")
    
    if model is None:
        st.warning("⚠️ Model not found. Run analysis.py first.")
    else:
        st.info("Enter customer details to predict churn risk")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tenure = st.number_input("Tenure (months)", 0, 72, 12)
            monthly = st.number_input("Monthly Charges ($)", 0.0, 200.0, 70.0)
            total = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0)
            senior = st.selectbox("Senior Citizen", [0, 1])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
        
        with col2:
            phone = st.selectbox("Phone Service", ["Yes", "No"])
            multiple = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
            internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
            backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
            protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        
        with col3:
            tech = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
            tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
            payment = st.selectbox("Payment Method", 
                                  ["Electronic check", "Mailed check", 
                                   "Bank transfer (automatic)", "Credit card (automatic)"])
            gender = st.selectbox("Gender", ["Male", "Female"])
        
        if st.button("🔮 Predict Churn Risk", type="primary"):
            # Create input dataframe
            input_data = pd.DataFrame({
                'gender': [gender],
                'SeniorCitizen': [senior],
                'Partner': [partner],
                'Dependents': [dependents],
                'tenure': [tenure],
                'PhoneService': [phone],
                'MultipleLines': [multiple],
                'InternetService': [internet],
                'OnlineSecurity': [security],
                'OnlineBackup': [backup],
                'DeviceProtection': [protection],
                'TechSupport': [tech],
                'StreamingTV': [tv],
                'StreamingMovies': [movies],
                'Contract': [contract],
                'PaperlessBilling': [paperless],
                'PaymentMethod': [payment],
                'MonthlyCharges': [monthly],
                'TotalCharges': [total]
            })
            
            # Predict
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100
            
            st.markdown("---")
            
            # Results
            col1, col2 = st.columns(2)
            
            with col1:
                if prediction == 1:
                    st.error(f"⚠️ HIGH RISK - Churn Probability: {probability:.1f}%")
                else:
                    st.success(f"✅ LOW RISK - Churn Probability: {probability:.1f}%")
            
            with col2:
                # Risk tier
                if probability >= 60:
                    tier = "🔴 High Risk"
                    color = "red"
                elif probability >= 30:
                    tier = "🟡 Medium Risk"
                    color = "orange"
                else:
                    tier = "🟢 Low Risk"
                    color = "green"
                
                st.markdown(f"### {tier}")
            
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability,
                title={'text': "Risk Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 60], 'color': "lightyellow"},
                        {'range': [60, 100], 'color': "lightcoral"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            if probability >= 60:
                st.markdown("### 💡 Recommended Actions:")
                st.markdown("""
                - 🎯 **Immediate outreach** within 48 hours
                - 💰 Offer retention incentive ($25-50 credit)
                - 📞 Schedule customer success call
                - 🎁 Provide service upgrade trial (3 months free)
                """)
            elif probability >= 30:
                st.markdown("### 💡 Recommended Actions:")
                st.markdown("""
                - 📧 Send engagement email campaign
                - 🔍 Monitor usage patterns weekly
                - 💳 Suggest contract upgrade with discount
                """)

# Footer
st.markdown("---")
st.markdown("**📧 Pavan Kumar Reddy** | Data Analyst Portfolio Project | 2026")