from pydantic import BaseModel
from typing import List, Optional


class MediaChannel(BaseModel):
	"""Represents a specific media channel with its details"""
	channel_name: str
	description: str
	budget_allocation: str
	target_audience: str
	content_strategy: str
	timing: str
	expected_reach: str
	success_metrics: List[str]


class MediaPlan(BaseModel):
	"""Complete media plan structure"""
	title: str
	overview: str
	total_budget: str
	campaign_duration: str
	primary_objectives: List[str]
	media_channels: List[MediaChannel]
	integrated_strategy: str
	risk_mitigation: List[str]
	success_measurement: List[str]
	implementation_timeline: str
	input_tokens: int = -1
	output_tokens: int = -1
