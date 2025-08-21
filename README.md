# AURA - Researcher Agent

A Streamlit application for generating marketing campaign briefs from market research and objectives.

## Project Structure

```
arena/
├── app.py                          # Main application entry point
├── researcher_agent.py             # Legacy entry point (backward compatibility)
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
    ├── constants.py                # Constants and Bedrock model IDs
    ├── prompt_templates.py         # Prompt templates
    └── token_cost.py               # Token cost calculations
```

## Usage

```bash
streamlit run app.py
# or
streamlit run researcher_agent.py
```

## Configuration
Change defaults in `config/settings.py` (model, region, temperature, limits, etc.).

## Dependencies
- `streamlit`, `aiolimiter`, `pydantic`, `langchain_aws`
- For file loading: `pdfplumber`, `python-docx`

Install extras as needed:
```bash
pip install pdfplumber python-docx
```
# understand streamlit
