import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") # Assuming Tavily for search

    # Model Configurations
    PLANNER_MODEL = "gpt-5"
    RESEARCHER_MODEL = "gpt-5"
    WRITER_MODEL = "gpt-5"
    REVIEWER_MODEL = "gpt-5"
    
    # Search Configuration
    MAX_SEARCH_RESULTS = 5
    SEARCH_PROVIDER = "tavily"

    # Memory Configuration
    WORKING_MEMORY_LIMIT = 4000 # Tokens
    
    # Stopping Criteria
    ISSP_THRESHOLD = 0.05 # Information Gain Threshold
    MAX_STEPS = 20
    
    # Paths
    DATA_DIR = "data"
    OUTPUT_DIR = "output"
