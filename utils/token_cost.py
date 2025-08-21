from typing import Tuple

# Costs are per 1K tokens
_MODEL_COSTS: dict[str, Tuple[float, float]] = {
	"sonnet": (0.003, 0.015),  # (input_per_1k, output_per_1k)
	"haiku": (0.00025, 0.00125),
}

def get_token_costs(model_name: str) -> Tuple[float, float]:
	"""Return (input_cost_per_1k, output_cost_per_1k) for the given model.
	Defaults to sonnet if unknown.
	"""
	return _MODEL_COSTS.get(model_name, _MODEL_COSTS["sonnet"])

