from langchain_openai import ChatOpenAI
from aiolimiter import AsyncLimiter
from typing import List
from models.campaign_brief import CampaignBrief
from config.settings import (
	MODEL, OPENAI_API_KEY, OPENAI_TEMPERATURE,
	OPENAI_TOP_P, OPENAI_MAX_TOKENS,
	RATE_LIMIT_MAX_RATE, RATE_LIMIT_TIME_PERIOD
)
from utils.constants import Constants
from utils.prompt_templates import Prompts

class BriefService:
	"""Service to generate a marketing campaign brief from research and objectives"""

	def __init__(self):
		if not OPENAI_API_KEY:
			raise ValueError("OPENAI_API_KEY environment variable is required")
		
		self.chat_model = ChatOpenAI(
			model=Constants.OPENAI_LLM_MODELS[MODEL],
			api_key=OPENAI_API_KEY,
			temperature=OPENAI_TEMPERATURE,
			top_p=OPENAI_TOP_P,
			max_tokens=OPENAI_MAX_TOKENS,
		)
		self.structured_llm = self.chat_model.with_structured_output(CampaignBrief, include_raw=True)
		self.limiter = AsyncLimiter(max_rate=RATE_LIMIT_MAX_RATE, time_period=RATE_LIMIT_TIME_PERIOD)

	async def generate_brief(self, research_text: str, objectives: str, system_prompt: str | None = None) -> CampaignBrief:
		"""Generate a structured campaign brief"""
		prompt = system_prompt or Prompts.campaign_brief_system_prompt
		# Truncate overly large inputs to avoid token limits (basic safeguard)
		context = research_text.strip()
		user = f"Objectives:\n{objectives.strip()}\n\nMarket Research:\n{context}"

		async with self.limiter:
			response = await self.structured_llm.ainvoke(
				(
					("system", prompt),
					("human", user),
				)
			)
			parsed: CampaignBrief = response["parsed"]
			parsed.input_tokens = response["raw"].usage_metadata.get("prompt_tokens", -1)
			parsed.output_tokens = response["raw"].usage_metadata.get("completion_tokens", -1)
			return parsed
