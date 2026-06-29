# src/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.analytics_engine import SalesAnalyticsEngine
import os

app = FastAPI(title="Sales Trend Visualization System")

# Establish explicit structural paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
TEMPLATES_PATH = os.path.join(BASE_DIR, "templates")

# Initialize Jinja2 UI Template router
templates = Jinja2Templates(directory=TEMPLATES_PATH)

# Instantiate our custom Pandas data engine
engine = SalesAnalyticsEngine(csv_path=DATA_PATH)

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    """Serves the primary layout dashboard template to the client browser"""
    # This explicit keyword format avoids internal positional parsing errors
    return templates.TemplateResponse(request=request, name="dashboard.html")

@app.get("/api/analytics")
async def get_analytics_data():
    """API Endpoint: Exposes calculated analytical metrics to frontend Chart.js hooks"""
    metrics = engine.process_sales_metrics()
    return metrics