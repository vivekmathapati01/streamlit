from typing import Tuple

# Costs are per 1K tokens (OpenAI pricing)
_MODEL_COSTS: dict[str, Tuple[float, float]] = {
	"gpt-4": (0.03, 0.06),  # (input_per_1k, output_per_1k)
	"gpt-4-turbo": (0.01, 0.03),  # (input_per_1k, output_per_1k)
	"gpt-4o": (0.005, 0.015),  # (input_per_1k, output_per_1k)
	"gpt-4o-mini": (0.00015, 0.0006),  # (input_per_1k, output_per_1k)
	"gpt-3.5-turbo": (0.0015, 0.002),  # (input_per_1k, output_per_1k)
}

def get_token_costs(model_name: str) -> Tuple[float, float]:
	"""Return (input_cost_per_1k, output_cost_per_1k) for the given model.
	Defaults to gpt-4-turbo if unknown.
	"""
	return _MODEL_COSTS.get(model_name, _MODEL_COSTS["gpt-4-turbo"])

