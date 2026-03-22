import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_data(num_rows=10000):
    """Generates a synthetic dataset for AI ROI Analysis."""
    
    np.random.seed(42)
    random.seed(42)

    # 1. Define Categories and their relative weights (Frequency)
    # Shipping Updates (40%), Product Questions (25%), Refund Requests (15%), 
    # Billing Inquiries (12%), Technical Issues (8%)
    categories = [
        "Shipping Update", "Product Question", "Refund Request", 
        "Billing Inquiry", "Technical Issue"
    ]
    category_weights = [0.40, 0.25, 0.15, 0.12, 0.08]

    # 2. Resolution Time Logic (Mean hours for each category)
    resolution_means = {
        "Shipping Update": 1.0,
        "Product Question": 3.0,
        "Refund Request": 2.0,
        "Billing Inquiry": 5.0,
        "Technical Issue": 24.0
    }

    # 3. Generate Core Data
    data = []
    start_date = datetime.now() - timedelta(days=365)

    for i in range(num_rows):
        ticket_id = f"TICK-{100000 + i}"
        
        # Timestamp distribution (uniform over last 12 months)
        random_days = random.random() * 365
        timestamp = start_date + timedelta(days=random_days)
        
        # Category selection based on weights
        category = random.choices(categories, weights=category_weights, k=1)[0]
        
        # Priority selection (weighted)
        priority = random.choices(
            ["Low", "Medium", "High"], 
            weights=[0.6, 0.3, 0.1], 
            k=1
        )[0]

        # Resolution time (log-normal distribution around the mean for realism)
        # Using lognormal ensures positive values and some outliers
        mean_hrs = resolution_means[category]
        resolution_time_hrs = max(0.1, np.random.lognormal(mean=np.log(mean_hrs), sigma=0.4))
        
        # Sentiment distribution
        sentiment = random.choices(
            ["Positive", "Neutral", "Negative"],
            weights=[0.2, 0.5, 0.3],
            k=1
        )[0]

        data.append({
            "ticket_id": ticket_id,
            "timestamp": timestamp,
            "category": category,
            "priority": priority,
            "resolution_time_hrs": round(resolution_time_hrs, 2),
            "customer_sentiment": sentiment
        })

    # 4. Create DataFrame and Sort
    df = pd.DataFrame(data)
    df = df.sort_values(by="timestamp").reset_index(drop=True)

    # 5. Save to CSV
    filename = "support_tickets_audit.csv"
    df.to_csv(filename, index=False)
    print(f"Successfully generated {num_rows} tickets and saved to {filename}")
    
    return df

if __name__ == "__main__":
    generate_synthetic_data()
