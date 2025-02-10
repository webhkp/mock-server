import os
import yaml
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date

app = FastAPI()

# Path for config file
config_file_path = os.getenv("CONFIG_FILE", "./config.yml")

# Load configuration
def load_config():
    try:
        with open(config_file_path, "r") as file:
            return yaml.safe_load(file) or {"routes": []}
    except Exception:
        return {"routes": []}

# Save configuration
def save_config(config):
    with open(config_file_path, "w") as file:
        yaml.safe_dump(config, file)

# Static directory and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load initial configuration
config = load_config()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    config_data = load_config()
    routes_data = config_data.get("routes", [])
    
    return templates.TemplateResponse("index.html", {"request": request, "routes_data": routes_data, 'current_year': date.today().year})

@app.post("/add-route")
def add_route(
    endpoint: str = Form(...),
    response_message: str = Form(...),
    response_status: str = Form("success")
):
    new_route = {
        "endpoint": endpoint,
        "response": {"status": response_status, "message": response_message}
    }
    config["routes"].append(new_route)
    save_config(config)
    
    load_route_from_config()
    
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

# Register dynamic routes based on the config file
def load_route_from_config():
    for route in config.get("routes", []):
        endpoint = route.get("endpoint", "/default")
        response = route.get("response", {})

        @app.get(endpoint)
        def dynamic_route(resp=response):
            return resp

load_route_from_config()