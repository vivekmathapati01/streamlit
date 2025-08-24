import streamlit as st
import asyncio
from typing import List
from services.brief_service import BriefService
from utils.file_loader import load_file_to_text
from config.settings import INPUT_COST, OUTPUT_COST
from ui.media_plan_generator import render_media_plan_generator


def _display_brief(brief):
	st.subheader("Campaign Brief")
	st.markdown(f"**Title**: {brief.title}")
	st.markdown("**Objective Summary**")
	st.write(brief.objective_summary)

	def _render_list(title: str, items: List[str]):
		if items:
			st.markdown(f"**{title}**")
			for it in items:
				st.write(f"- {it}")

	_render_list("Target Audience", brief.target_audience)
	_render_list("Key Insights", brief.key_insights)
	st.markdown("**Value Proposition**")
	st.write(brief.value_proposition)
	_render_list("Messaging Pillars", brief.messaging_pillars)
	_render_list("Recommended Channels", brief.channels)
	_render_list("Recommendations", brief.recommendations)
	_render_list("KPIs", brief.kpis)
	if brief.budget_guidance:
		st.markdown("**Budget Guidance**")
		st.write(brief.budget_guidance)
	if brief.timeline:
		st.markdown("**Timeline**")
		st.write(brief.timeline)

	col_a, col_b, col_c = st.columns(3)
	col_a.metric("Input Tokens", brief.input_tokens)
	col_b.metric("Output Tokens", brief.output_tokens)
	col_c.metric(
		"Cost (in $)",
		f"{(brief.input_tokens * INPUT_COST/1000 + brief.output_tokens * OUTPUT_COST/1000):.4f}",
		help="Estimated cost based on token usage"
	)


def render_brief_generator():
	st.header("Generate Marketing Campaign Brief")

	# Upload research files
	uploaded_files = st.file_uploader(
		"Upload market research files (PDF, DOCX, TXT, CSV)", type=["pdf", "docx", "txt", "csv"], accept_multiple_files=True
	)

	# Objectives input
	objectives = st.text_area("Enter marketing objectives", height=120)

	# Optional system prompt override
	advanced = st.expander("Advanced settings", expanded=False)
	with advanced:
		custom_prompt = st.text_area("System prompt (optional)", value="")

	if st.button("Generate Brief"):
		if not objectives.strip():
			st.warning("Please enter marketing objectives.")
			return
		if not uploaded_files:
			st.warning("Please upload at least one research file.")
			return

		with st.spinner("Generating brief..."):
			# Load research files into a single context string
			texts: List[str] = []
			for uf in uploaded_files:
				try:
					texts.append(load_file_to_text(uf.name, uf.getvalue()))
				except Exception as e:
					st.error(f"Failed to read {uf.name}: {e}")
					return
			research_context = "\n\n".join(texts)

			service = BriefService()
			brief = asyncio.run(service.generate_brief(research_context, objectives, custom_prompt or None))

			# Store in session state (key change)
			st.session_state.campaign_brief = brief
			st.session_state.media_plan = None
			st.session_state.media_plan_generated = False
			st.session_state.media_plan_key = 0

	# Always show brief if it exists
	if "campaign_brief" in st.session_state:
		_display_brief(st.session_state.campaign_brief)

	# Always show media plan generator if brief exists
	if "campaign_brief" in st.session_state:
		render_media_plan_generator(st.session_state.campaign_brief)
