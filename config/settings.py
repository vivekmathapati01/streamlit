from utils.token_cost import get_token_costs
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model configuration
MODEL = "gpt-4-turbo"  # Change this to "gpt-4" or "gpt-3.5-turbo" as needed
INPUT_COST, OUTPUT_COST = get_token_costs(MODEL)

# Rate limiter configuration
RATE_LIMIT_MAX_RATE = 50
RATE_LIMIT_TIME_PERIOD = 60

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "***REMOVED***")
OPENAI_TEMPERATURE = 0
OPENAI_TOP_P = 0
OPENAI_MAX_TOKENS = 4096
