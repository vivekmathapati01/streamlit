from pydantic import BaseModel
from typing import List, Optional

class CampaignBrief(BaseModel):
	"""Structured marketing campaign brief"""
	title: str
	objective_summary: str
	target_audience: List[str]
	key_insights: List[str]
	value_proposition: str
	messaging_pillars: List[str]
	channels: List[str]
	recommendations: List[str]
	kpis: List[str]
	budget_guidance: Optional[str] = None
	timeline: Optional[str] = None

	# token accounting
	input_tokens: int = -1
	output_tokens: int = -1
