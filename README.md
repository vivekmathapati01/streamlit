# Marketing Campaign Brief Generator

A Streamlit application for generating marketing campaign briefs from market research and objectives using OpenAI's GPT models.

## Features

- Upload market research files (PDF, DOCX, TXT, CSV)
- Generate structured marketing campaign briefs
- Cost tracking based on token usage
- Rate limiting for API calls
- Support for multiple OpenAI models (GPT-4, GPT-4 Turbo, GPT-3.5 Turbo)

## Project Structure

```
streamlit/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── models/
│   ├── __init__.py
│   └── campaign_brief.py           # Pydantic model for campaign brief
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration settings
├── services/
│   ├── __init__.py
│   └── brief_service.py            # AI/LLM interaction for brief generation
├── ui/
│   ├── __init__.py
│   └── brief_generator.py          # Upload research + objectives → Campaign brief
└── utils/
    ├── __init__.py
    ├── file_loader.py              # Extract text from PDF/DOCX/TXT research files
    ├── constants.py                # Constants and OpenAI model IDs
    ├── prompt_templates.py         # Prompt templates
    └── token_cost.py               # Token cost calculations
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Configuration

You can modify the following settings in `config/settings.py`:

- **Model**: Change `MODEL` to use different OpenAI models:
  - `"gpt-4"` - Most capable but expensive
  - `"gpt-4-turbo"` - Good balance of capability and cost (default)
  - `"gpt-4o"` - Latest model with good performance
  - `"gpt-4o-mini"` - Fast and very cost-effective
  - `"gpt-3.5-turbo"` - Fastest and cheapest

- **Generation parameters**: Adjust temperature, top_p, and max_tokens
- **Rate limiting**: Modify rate limits for API calls

## Usage

1. Upload your market research files (PDF, DOCX, TXT, or CSV format)
2. Enter your marketing objectives
3. Optionally customize the system prompt in advanced settings
4. Click "Generate Brief" to create a structured campaign brief

The application will display:
- Campaign title and objective summary
- Target audience and key insights
- Value proposition and messaging pillars
- Recommended channels and KPIs
- Budget guidance and timeline
- Token usage and estimated cost

## Dependencies

- **Core**: `streamlit`, `openai`, `langchain`, `langchain-openai`
- **File processing**: `python-docx`, `pdfplumber`, `pandas`
- **Utilities**: `aiolimiter`, `pydantic`, `python-dotenv`

## Cost Tracking

The application tracks token usage and estimates costs based on OpenAI's pricing:
- GPT-4: $0.03/1K input tokens, $0.06/1K output tokens
- GPT-4 Turbo: $0.01/1K input tokens, $0.03/1K output tokens
- GPT-4o: $0.005/1K input tokens, $0.015/1K output tokens
- GPT-4o-mini: $0.00015/1K input tokens, $0.0006/1K output tokens
- GPT-3.5 Turbo: $0.0015/1K input tokens, $0.002/1K output tokens
