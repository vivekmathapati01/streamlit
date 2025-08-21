import streamlit as st
from ui.brief_generator import render_brief_generator


def main():
	"""Main application entry point"""
	st.title("AURA - Researcher Agent")

	# Render brief generator only
	render_brief_generator()


if __name__ == "__main__":
	main()
