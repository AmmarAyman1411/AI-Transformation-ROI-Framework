# AI Business Analyst & ROI Strategy Framework 🚀

An end-to-end framework for simulating, analyzing, and visualizing the ROI of implementing an AI Agent in a mid-sized E-commerce support environment.

## 📌 Project Overview
This project provides a data-driven approach to justify AI transformation. It transitions from raw synthetic data generation to a sophisticated financial model (Monte Carlo simulation) and finally an interactive C-Suite dashboard.

### **Core Modules**
1. **[data_generator.py](data_generator.py):** Generates 10,000 synthetic support tickets with realistic distributions (category, priority, resolution time, sentiment).
2. **[audit_analyzer.py](audit_analyzer.py):** Performs a "Business Audit" to calculate the current 'As-Is' labor costs and identify automation potential per category.
3. **[roi_engine.py](roi_engine.py):** A robust simulation engine that runs 1,000 Monte Carlo iterations to predict net savings, factoring in API costs, maintenance, and setup fees.
4. **[app.py](app.py):** A Streamlit-based interactive dashboard for real-time ROI sensitivity analysis.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Data Science:** `pandas`, `numpy`, `scipy`
- **Visualization:** `plotly`, `streamlit`

---

## 🚀 Getting Started

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd AI-Transformation-ROI-Framework
```

### **2. Setup Environment**
Create and activate a virtual environment:
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the Framework**
To generate the data and launch the dashboard:
```bash
# 1. Generate synthetic logs
python data_generator.py

# 2. Run the Streamlit Dashboard
streamlit run app.py
```

---

## 📊 Methodology
### **Monte Carlo Simulation**
Unlike static spreadsheets, our ROI Engine accounts for real-world variability. It simulates 12 months of operations 1,000 times, varying:
- **Monthly Ticket Volume:** Normal distribution with 5% variance.
- **AI Deflection Rate:** Modeled with a clip to maintain realistic bounds.

### **Automation Potential**
We assume different "Success Rates" for AI based on category complexity:
- **Refund Requests:** 90% (High repeatability)
- **Technical Issues:** 20% (High complexity)
- **Shipping Updates:** 85% (Data retrieval focus)

---

## 📄 License
This project is open-source and available under the MIT License.
