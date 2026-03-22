import numpy as np
import pandas as pd

class ROIEngine:
    def __init__(self, setup_fee=50000, monthly_maintenance=2000, api_cost_per_ticket=0.01):
        self.setup_fee = setup_fee
        self.monthly_maintenance = monthly_maintenance
        self.api_cost_per_ticket = api_cost_per_ticket

    def simulate_roi(self, monthly_ticket_volume, deflection_rate, agent_hourly_rate, avg_resolution_time, num_runs=1000):
        """Runs a Monte Carlo simulation to predict 12-month ROI."""
        
        all_runs_savings = []
        all_runs_costs = []
        
        # We vary deflection rate and ticket volume slightly for realism
        for _ in range(num_runs):
            # Normal distribution with some variance for monthly volume and deflection
            monthly_vol_sim = np.random.normal(monthly_ticket_volume, monthly_ticket_volume * 0.05, 12)
            deflection_sim = np.random.normal(deflection_rate, 0.05, 12)
            deflection_sim = np.clip(deflection_sim, 0, 0.95) # Clip to reasonable bounds
            
            monthly_gross_savings = []
            monthly_ai_costs = []
            
            for m in range(12):
                tickets_deflected = monthly_vol_sim[m] * deflection_sim[m]
                # Savings = (Deflected Tickets) * (Avg Resolution Time) * (Agent Rate)
                savings = tickets_deflected * avg_resolution_time * agent_hourly_rate
                
                # Costs = Maintenance + (Deflected Tickets * API Cost)
                costs = self.monthly_maintenance + (tickets_deflected * self.api_cost_per_ticket)
                
                monthly_gross_savings.append(savings)
                monthly_ai_costs.append(costs)
            
            cumulative_net_savings = np.cumsum(monthly_gross_savings) - np.cumsum(monthly_ai_costs) - self.setup_fee
            all_runs_savings.append(cumulative_net_savings)

        return np.array(all_runs_savings)

    def calculate_payback_period(self, simulation_results):
        """Calculates the average month where cumulative savings turn positive."""
        avg_savings_over_time = np.mean(simulation_results, axis=0)
        payback_month = next((i + 1 for i, v in enumerate(avg_savings_over_time) if v > 0), None)
        return payback_month, avg_savings_over_time

if __name__ == "__main__":
    # Quick test run
    engine = ROIEngine()
    # Assume 10,000 tickets / 12 months = ~833 tickets/month
    # Assume 70% deflection, $25/hr rate, 4h average resolution time
    results = engine.simulate_roi(833, 0.70, 25, 4)
    payback, avg_savings = engine.calculate_payback_period(results)
    
    print(f"--- ROI Engine Simulation ---")
    print(f"Average Payback Period: {payback} months")
    print(f"Total Net Savings after 12 months: ${avg_savings[-1]:,.2f}")
