# src/analytics_engine.py
import pandas as pd
import os

class SalesAnalyticsEngine:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def process_sales_metrics(self) -> dict:
        """Reads raw sales CSV and structures complex metrics for charting"""
        if not os.path.exists(self.csv_path):
            return {"error": "Sales data repository asset missing"}

        # Load data into a Pandas DataFrame
        df = pd.read_csv(self.csv_path)
        
        # Ensure dates are correctly typed and extract Month strings
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.strftime('%B') # e.g., "January", "February"

        # 1. Timeline Trend Aggregation (For Line Graph)
        monthly_summary = df.groupby('Month', sort=False)[['Revenue', 'Units_Sold']].sum().reset_index()
        months_labels = monthly_summary['Month'].tolist()
        revenue_trends = monthly_summary['Revenue'].tolist()

        # 2. Product Category Contribution Aggregation (For Bar Chart)
        category_summary = df.groupby('Product_Category')['Revenue'].sum().reset_index()
        categories_labels = category_summary['Product_Category'].tolist()
        category_revenues = category_summary['Revenue'].tolist()

        # 3. High-level Summary Metrics Cards
        total_revenue = int(df['Revenue'].sum())
        total_units = int(df['Units_Sold'].sum())
        avg_transaction = round(df['Revenue'].mean(), 2)

        return {
            "charts": {
                "timeline_months": months_labels,
                "timeline_revenue": revenue_trends,
                "category_labels": categories_labels,
                "category_data": category_revenues
            },
            "kpis": {
                "total_revenue": total_revenue,
                "total_units_sold": total_units,
                "average_order_value": avg_transaction
            }
        }