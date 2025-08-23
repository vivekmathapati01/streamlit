import streamlit as st
import asyncio
from typing import List
from services.brief_service import BriefService
from utils.file_loader import load_file_to_text
from config.settings import INPUT_COST, OUTPUT_COST


def _display_brief(brief):
	st.subheader("Campaign Brief")
	
	# Format the brief as text
	brief_text = f"""CAMPAIGN BRIEF

Title: {brief.title}

OBJECTIVE SUMMARY
{brief.objective_summary}

TARGET AUDIENCE"""
	
	if brief.target_audience:
		for item in brief.target_audience:
			brief_text += f"\n• {item}"
	
	brief_text += "\n\nKEY INSIGHTS"
	if brief.key_insights:
		for item in brief.key_insights:
			brief_text += f"\n• {item}"
	
	brief_text += f"""

VALUE PROPOSITION
{brief.value_proposition}

MESSAGING PILLARS"""
	if brief.messaging_pillars:
		for item in brief.messaging_pillars:
			brief_text += f"\n• {item}"
	
	brief_text += "\n\nRECOMMENDED CHANNELS"
	if brief.channels:
		for item in brief.channels:
			brief_text += f"\n• {item}"
	
	brief_text += "\n\nRECOMMENDATIONS"
	if brief.recommendations:
		for item in brief.recommendations:
			brief_text += f"\n• {item}"
	
	brief_text += "\n\nKPIs"
	if brief.kpis:
		for item in brief.kpis:
			brief_text += f"\n• {item}"
	
	if brief.budget_guidance:
		brief_text += f"\n\nBUDGET GUIDANCE\n{brief.budget_guidance}"
	
	if brief.timeline:
		brief_text += f"\n\nTIMELINE\n{brief.timeline}"
	
	# Display in text area
	st.text_area(
		"Generated Campaign Brief",
		value=brief_text,
		height=600,
		help="Copy this text to use in your marketing campaigns"
	)
	
	# Display metrics below the text area
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
			_display_brief(brief)
