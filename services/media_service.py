from langchain_openai import ChatOpenAI
from aiolimiter import AsyncLimiter
from typing import List
from models.media_plan import MediaPlan
from models.campaign_brief import CampaignBrief
from config.settings import (
	MODEL, OPENAI_API_KEY, OPENAI_TEMPERATURE,
	OPENAI_TOP_P, OPENAI_MAX_TOKENS,
	RATE_LIMIT_MAX_RATE, RATE_LIMIT_TIME_PERIOD
)
from utils.constants import Constants
from utils.prompt_templates import Prompts

class MediaService:
	"""Service to generate a media plan from campaign brief"""

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
		self.structured_llm = self.chat_model.with_structured_output(MediaPlan, include_raw=True)
		self.limiter = AsyncLimiter(max_rate=RATE_LIMIT_MAX_RATE, time_period=RATE_LIMIT_TIME_PERIOD)

	async def generate_media_plan(self, campaign_brief: CampaignBrief, custom_prompt: str | None = None) -> MediaPlan:
		"""Generate a structured media plan based on the campaign brief"""
		prompt = custom_prompt or Prompts.media_plan_system_prompt
		
		# Convert campaign brief to text format for the AI
		brief_text = self._format_brief_for_media_plan(campaign_brief)
		user = f"Campaign Brief:\n{brief_text}"

		async with self.limiter:
			try:
				response = await self.structured_llm.ainvoke(
					(
						("system", prompt),
						("human", user),
					)
				)
				print("media response: ", response)
				parsed: MediaPlan = response["parsed"]
				parsed.input_tokens = response["raw"].usage_metadata.get("prompt_tokens", -1)
				parsed.output_tokens = response["raw"].usage_metadata.get("completion_tokens", -1)
				return parsed
			except Exception as e:
				import traceback
				error_details = traceback.format_exc()
				raise Exception(f"Failed to generate media plan: {str(e)}\nDetails: {error_details}")

	def _format_brief_for_media_plan(self, brief: CampaignBrief) -> str:
		"""Format the campaign brief into a structured text for media plan generation"""
		text_parts = [
			f"Title: {brief.title}",
			f"Objective Summary: {brief.objective_summary}",
			f"Value Proposition: {brief.value_proposition}"
		]
		
		if brief.target_audience:
			text_parts.append(f"Target Audience: {', '.join(brief.target_audience)}")
		
		if brief.key_insights:
			text_parts.append(f"Key Insights: {', '.join(brief.key_insights)}")
		
		if brief.messaging_pillars:
			text_parts.append(f"Messaging Pillars: {', '.join(brief.messaging_pillars)}")
		
		if brief.channels:
			text_parts.append(f"Recommended Channels: {', '.join(brief.channels)}")
		
		if brief.recommendations:
			text_parts.append(f"Recommendations: {', '.join(brief.recommendations)}")
		
		if brief.kpis:
			text_parts.append(f"KPIs: {', '.join(brief.kpis)}")
		
		if brief.budget_guidance:
			text_parts.append(f"Budget Guidance: {brief.budget_guidance}")
		
		if brief.timeline:
			text_parts.append(f"Timeline: {brief.timeline}")
		
		return "\n".join(text_parts)
