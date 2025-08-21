from utils.token_cost import get_token_costs

# Model configuration
MODEL = "sonnet"  # Change this to "haiku" as needed
INPUT_COST, OUTPUT_COST = get_token_costs(MODEL)

# Rate limiter configuration
RATE_LIMIT_MAX_RATE = 50
RATE_LIMIT_TIME_PERIOD = 60

# Bedrock configuration
BEDROCK_REGION = "ap-south-1"
BEDROCK_TEMPERATURE = 0
BEDROCK_TOP_P = 0
BEDROCK_MAX_TOKENS = 4096
