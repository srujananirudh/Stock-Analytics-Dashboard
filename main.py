from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# ✅ Enable CORS (VERY IMPORTANT for HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load dataset
df = pd.read_csv("data_clean/final_dataset.csv")

# ✅ Home route
@app.get("/")
def home():
    return {"message": "API running 🚀"}

# ✅ Data route (IMPORTANT: NO head())
@app.get("/data")
def get_data():
    return df.to_dict(orient="records")