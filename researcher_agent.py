from app import main

def streamlit_ui():
    """Legacy function for backward compatibility"""
    main()

def run():
    """Entry point for the application"""
    main()

if __name__ == "__main__":
    main()