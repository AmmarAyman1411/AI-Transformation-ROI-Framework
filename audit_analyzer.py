import pandas as pd

def perform_business_audit(csv_path="support_tickets_audit.csv"):
    """Analyzes the support data to calculate costs and automation potential."""
    
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 1. Constants
    AGENT_HOURLY_RATE = 25.0
    
    # 2. Automation Potential (User-defined/Industry standards)
    automation_potential = {
        "Refund Request": 0.90,
        "Technical Issue": 0.20,
        "Billing Inquiry": 0.70,
        "Product Question": 0.60,
        "Shipping Update": 0.85
    }

    # 3. Calculate Monthly Statistics
    # We have 12 months of data, let's group by month
    df['month_year'] = df['timestamp'].dt.to_period('M')
    
    # Calculate labor cost per ticket
    df['labor_cost'] = df['resolution_time_hrs'] * AGENT_HOURLY_RATE
    
    # Calculate potential savings per ticket
    df['potential_savings'] = df.apply(
        lambda x: x['labor_cost'] * automation_potential.get(x['category'], 0), 
        axis=1
    )

    # 4. Aggregate findings
    audit_results = df.groupby('category').agg({
        'ticket_id': 'count',
        'resolution_time_hrs': 'mean',
        'labor_cost': 'sum'
    }).rename(columns={'ticket_id': 'ticket_count', 'resolution_time_hrs': 'avg_resolution_time'})

    audit_results['automation_potential'] = audit_results.index.map(automation_potential)
    audit_results['potential_monthly_savings'] = (
        audit_results['labor_cost'] * audit_results['automation_potential']
    ) / 12  # Average over 12 months

    # Calculate Total Monthly Labor Cost
    total_labor_cost = df['labor_cost'].sum()
    avg_monthly_labor_cost = total_labor_cost / 12

    print("--- Business Audit Summary ---")
    print(f"Average Monthly Labor Cost: ${avg_monthly_labor_cost:,.2f}")
    print("\nBreakdown by Category:")
    print(audit_results[['ticket_count', 'avg_resolution_time', 'automation_potential', 'potential_monthly_savings']])
    
    return audit_results, avg_monthly_labor_cost

if __name__ == "__main__":
    perform_business_audit()
