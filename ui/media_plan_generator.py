import streamlit as st
from typing import List
from models.media_plan import MediaPlan
from config.settings import INPUT_COST, OUTPUT_COST


def _display_media_plan(media_plan: MediaPlan):
	"""Display the generated media plan in a structured format"""
	st.subheader("Media Plan")
	
	# Create a container with border styling
	with st.container():
		st.markdown("---")
		
		# Title section
		st.markdown(f"### 📺 {media_plan.title}")
		st.markdown("---")
		
		# Overview
		st.markdown("#### 📋 Overview")
		st.info(media_plan.overview)
		
		# Budget and Duration
		col1, col2 = st.columns(2)
		with col1:
			st.metric("Total Budget", media_plan.total_budget)
		with col2:
			st.metric("Campaign Duration", media_plan.campaign_duration)
		
		# Primary Objectives
		if media_plan.primary_objectives:
			st.markdown("#### 🎯 Primary Objectives")
			for objective in media_plan.primary_objectives:
				st.markdown(f"• {objective}")
		
		# Media Channels
		if media_plan.media_channels:
			st.markdown("#### 📡 Media Channels")
			for i, channel in enumerate(media_plan.media_channels, 1):
				with st.expander(f"{i}. {channel.channel_name}", expanded=True):
					st.markdown(f"**Description:** {channel.description}")
					st.markdown(f"**Budget Allocation:** {channel.budget_allocation}")
					st.markdown(f"**Target Audience:** {channel.target_audience}")
					st.markdown(f"**Content Strategy:** {channel.content_strategy}")
					st.markdown(f"**Timing:** {channel.timing}")
					st.markdown(f"**Expected Reach:** {channel.expected_reach}")
					
					if channel.success_metrics:
						st.markdown("**Success Metrics:**")
						for metric in channel.success_metrics:
							st.markdown(f"• {metric}")
		
		# Integrated Strategy
		st.markdown("#### 🔗 Integrated Strategy")
		st.success(media_plan.integrated_strategy)
		
		# Risk Mitigation
		if media_plan.risk_mitigation:
			st.markdown("#### ⚠️ Risk Mitigation")
			for risk in media_plan.risk_mitigation:
				st.markdown(f"• {risk}")
		
		# Success Measurement
		if media_plan.success_measurement:
			st.markdown("#### 📊 Success Measurement")
			for measurement in media_plan.success_measurement:
				st.markdown(f"• {measurement}")
		
		# Implementation Timeline
		st.markdown("#### ⏰ Implementation Timeline")
		st.info(media_plan.implementation_timeline)
		
		st.markdown("---")
	
	# Display metrics in a separate section
	st.markdown("### 📈 Usage Metrics")
	col_a, col_b, col_c = st.columns(3)
	col_a.metric("Input Tokens", media_plan.input_tokens)
	col_b.metric("Output Tokens", media_plan.output_tokens)
	col_c.metric(
		"Cost (in $)",
		f"{(media_plan.input_tokens * INPUT_COST/1000 + media_plan.output_tokens * OUTPUT_COST/1000):.4f}",
		help="Estimated cost based on token usage"
	)


def render_media_plan_generator(campaign_brief):
	"""Render the media plan generator section"""
	st.markdown("---")
	st.markdown("### 📺 Generate Media Plan")
	
	# Initialize session state for media plan
	if 'media_plan' not in st.session_state:
		st.session_state.media_plan = None
	if 'media_plan_generated' not in st.session_state:
		st.session_state.media_plan_generated = False
	if 'media_plan_key' not in st.session_state:
		st.session_state.media_plan_key = 0
	
	# Default media planning prompt
	default_media_prompt = """You are a senior media planning expert. Based on the provided campaign brief, create a comprehensive media plan that includes:

1. Specific media channels with detailed budget allocations
2. Target audience segmentation for each channel
3. Content strategy and messaging approach
4. Timing and frequency recommendations
5. Expected reach and engagement metrics
6. Success measurement criteria
7. Risk mitigation strategies
8. Implementation timeline

Focus on creating an integrated media strategy that maximizes ROI and aligns with the campaign objectives."""
	
	# Optional custom prompt for media plan
	advanced_media = st.expander("Advanced media planning settings", expanded=False)
	with advanced_media:
		custom_media_prompt = st.text_area("Media planning system prompt (optional)", value=default_media_prompt)
	
	# Direct button approach - handle everything in the button click
	if st.button("Generate Media Plan", key=f"generate_media_{st.session_state.media_plan_key}", type="primary"):
		if not campaign_brief:
			st.warning("Please generate a campaign brief first.")
		else:
			try:
				with st.spinner("Generating media plan..."):
					from services.media_service import MediaService
					import asyncio
					
					service = MediaService()
					media_plan = asyncio.run(service.generate_media_plan(
						campaign_brief, 
						custom_media_prompt or default_media_prompt
					))
					
					# Store the media plan in session state
					st.session_state.media_plan = media_plan
					st.session_state.media_plan_generated = True
					
			except Exception as e:
				st.error(f"Error generating media plan: {str(e)}")
				st.error("Please check your OpenAI API key and try again.")
	
	# Regenerate button
	if st.session_state.media_plan:
		if st.button("Regenerate Media Plan", key=f"regenerate_media_{st.session_state.media_plan_key}", type="secondary"):
			st.session_state.media_plan = None
			st.session_state.media_plan_generated = False
			st.session_state.media_plan_key += 1
	
	# Display the media plan if it exists in session state
	if st.session_state.media_plan:
		_display_media_plan(st.session_state.media_plan)
	else:
		# Debug info
		st.info("No media plan generated yet. Click 'Generate Media Plan' to create one.")
		st.write("Debug - Media plan state:", st.session_state.media_plan is not None)
		st.write("Debug - Media plan generated:", st.session_state.media_plan_generated)
