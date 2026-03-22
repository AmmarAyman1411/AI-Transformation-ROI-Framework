import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from roi_engine import ROIEngine

# Page Configuration
st.set_page_config(page_title="AI ROI Dashboard", layout="wide")

st.title("🚀 AI Business Analyst & ROI Strategy Dashboard")
st.markdown("""
### End-to-End ROI Simulation for AI Agent Implementation
This dashboard calculates the potential savings and payback period for implementing an AI Agent 
to handle customer support tickets.
""")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Simulation Parameters")

annual_volume = st.sidebar.slider("Annual Ticket Volume", 1000, 50000, 10000)
deflection_rate = st.sidebar.slider("AI Deflection Rate (%)", 10, 95, 70) / 100
agent_rate = st.sidebar.slider("Agent Hourly Rate ($)", 15, 60, 25)
avg_res_time = st.sidebar.slider("Avg Resolution Time (hrs)", 0.5, 24.0, 4.0)

st.sidebar.markdown("---")
st.sidebar.header("💰 Costs")
setup_fee = st.sidebar.number_input("One-time Setup Fee ($)", value=50000)
maintenance_fee = st.sidebar.number_input("Monthly Maintenance Fee ($)", value=2000)
api_cost = st.sidebar.number_input("API Cost per Ticket ($)", value=0.01)

# --- Simulation Execution ---
engine = ROIEngine(setup_fee, maintenance_fee, api_cost)
monthly_volume = annual_volume / 12

# Run Simulation
simulation_results = engine.simulate_roi(
    monthly_volume, 
    deflection_rate, 
    agent_rate, 
    avg_res_time, 
    num_runs=1000
)

# Calculate metrics
payback_month, avg_savings = engine.calculate_payback_period(simulation_results)
total_savings = avg_savings[-1]
roi_percentage = (total_savings / setup_fee) * 100 if setup_fee > 0 else 0

# --- Metrics Display ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total 12-Month Net Savings", f"${total_savings:,.2f}", delta=f"{roi_percentage:,.1f}% ROI")

with col2:
    if payback_month:
        st.metric("Payback Period", f"{payback_month} Months")
    else:
        st.metric("Payback Period", "N/A (> 12 Months)")

with col3:
    monthly_gross_savings = (monthly_volume * deflection_rate * avg_res_time * agent_rate)
    st.metric("Avg Monthly Gross Savings", f"${monthly_gross_savings:,.2f}")

# --- Visualization ---
st.markdown("### Cumulative Savings vs. Investment Over Time")

months = [f"Month {i+1}" for i in range(12)]
fig = go.Figure()

# Plot Cumulative Savings
fig.add_trace(go.Scatter(
    x=months, 
    y=avg_savings,
    mode='lines+markers',
    name='Cumulative Net Savings',
    line=dict(color='green', width=4)
))

# Plot Break-even Line
fig.add_trace(go.Scatter(
    x=months,
    y=[0]*12,
    mode='lines',
    name='Break-even Point',
    line=dict(color='red', dash='dash')
))

# Plot Initial Investment (Negative Setup Fee)
fig.add_trace(go.Scatter(
    x=months,
    y=[-setup_fee]*12,
    mode='lines',
    name='Initial Investment',
    line=dict(color='orange', dash='dot')
))

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Cumulative Net Profit/Loss ($)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# --- Summary & Insights ---
st.markdown("### 💡 Key Strategic Insights")
with st.expander("Show Detailed Insights"):
    st.write(f"""
    - **Efficiency Gains:** Automating {deflection_rate*100:.0f}% of tickets would save roughly 
    {(annual_volume * deflection_rate * avg_res_time):,.0f} human hours per year.
    - **Resource Allocation:** This allows your team to focus on high-complexity issues 
    (like 'Technical Issues' which only have 20% automation potential).
    - **Financial Impact:** After the {payback_month if payback_month else '>12'}-month payback period, 
    the AI Agent generates pure profit for the support department.
    """)
