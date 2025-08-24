from __future__ import annotations
from typing import List
import io

try:
	import docx  # python-docx
except Exception:
	docx = None

try:
	import pdfplumber
except Exception:
	pdfplumber = None

try:
	import pandas as pd
except Exception:
	pd = None

try:
	import openpyxl
except Exception:
	openpyxl = None


def _read_txt(file_bytes: bytes) -> str:
	return file_bytes.decode("utf-8", errors="ignore")


def _read_docx(file_bytes: bytes) -> str:
	if not docx:
		raise RuntimeError("python-docx is not installed")
	buf = io.BytesIO(file_bytes)
	document = docx.Document(buf)
	return "\n".join(p.text for p in document.paragraphs)


def _read_pdf(file_bytes: bytes) -> str:
	if not pdfplumber:
		raise RuntimeError("pdfplumber is not installed")
	buf = io.BytesIO(file_bytes)
	text_parts: List[str] = []
	with pdfplumber.open(buf) as pdf:
		for page in pdf.pages:
			text_parts.append(page.extract_text() or "")
	return "\n".join(text_parts)


def _read_excel(file_bytes: bytes) -> str:
	if not pd:
		raise RuntimeError("pandas is not installed")
	
	buf = io.BytesIO(file_bytes)
	text_parts = []
	
	try:
		# Read all sheets from the Excel file
		excel_file = pd.ExcelFile(buf)
		sheet_names = excel_file.sheet_names
		
		text_parts.append(f"Excel File Analysis")
		text_parts.append(f"Number of sheets: {len(sheet_names)}")
		text_parts.append(f"Sheet names: {', '.join(sheet_names)}")
		text_parts.append("")
		
		# Process each sheet
		for sheet_name in sheet_names:
			text_parts.append(f"=== Sheet: {sheet_name} ===")
			
			# Read the sheet
			df = pd.read_excel(buf, sheet_name=sheet_name)
			
			# Add sheet information
			text_parts.append(f"Columns: {', '.join(df.columns.tolist())}")
			text_parts.append(f"Rows: {len(df)}")
			text_parts.append("")
			
			# Add sample data (first 10 rows)
			if len(df) > 0:
				text_parts.append("Sample Data (first 10 rows):")
				text_parts.append(df.head(10).to_string(index=False))
				text_parts.append("")
				
				# Add basic statistics for numeric columns
				numeric_cols = df.select_dtypes(include=['number']).columns
				if len(numeric_cols) > 0:
					text_parts.append("Numeric Column Statistics:")
					text_parts.append(df[numeric_cols].describe().to_string())
					text_parts.append("")
				
				# Add value counts for categorical columns (first few categories)
				categorical_cols = df.select_dtypes(include=['object']).columns
				if len(categorical_cols) > 0:
					text_parts.append("Categorical Column Value Counts (top 5):")
					for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
						text_parts.append(f"\n{col}:")
						value_counts = df[col].value_counts().head(5)
						for value, count in value_counts.items():
							text_parts.append(f"  {value}: {count}")
					text_parts.append("")
			else:
				text_parts.append("Sheet is empty.")
				text_parts.append("")
			
			# Reset buffer position for next sheet
			buf.seek(0)
		
		return "\n".join(text_parts)
		
	except Exception as e:
		# Fallback: try to read as a single sheet
		buf.seek(0)
		try:
			df = pd.read_excel(buf)
			return _format_dataframe_text(df, "Excel Data")
		except Exception as e2:
			raise RuntimeError(f"Failed to read Excel file: {str(e2)}")


def _read_csv(file_bytes: bytes) -> str:
	if not pd:
		raise RuntimeError("pandas is not installed")
	buf = io.BytesIO(file_bytes)
	try:
		# Try to read CSV with default settings
		df = pd.read_csv(buf)
	except Exception:
		# If that fails, try with different encoding
		buf.seek(0)
		df = pd.read_csv(buf, encoding='latin-1')
	
	return _format_dataframe_text(df, "CSV Data")


def _format_dataframe_text(df: pd.DataFrame, title: str) -> str:
	"""Helper function to format DataFrame as text."""
	text_parts = []
	
	# Add title and basic info
	text_parts.append(f"{title}:")
	text_parts.append(f"Columns: {', '.join(df.columns.tolist())}")
	text_parts.append(f"Rows: {len(df)}")
	text_parts.append("")
	
	# Add sample data
	if len(df) > 0:
		text_parts.append("Sample Data (first 10 rows):")
		text_parts.append(df.head(10).to_string(index=False))
		text_parts.append("")
		
		# Add basic statistics for numeric columns
		numeric_cols = df.select_dtypes(include=['number']).columns
		if len(numeric_cols) > 0:
			text_parts.append("Numeric Column Statistics:")
			text_parts.append(df[numeric_cols].describe().to_string())
			text_parts.append("")
		
		# Add value counts for categorical columns (first few categories)
		categorical_cols = df.select_dtypes(include=['object']).columns
		if len(categorical_cols) > 0:
			text_parts.append("Categorical Column Value Counts (top 5):")
			for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
				text_parts.append(f"\n{col}:")
				value_counts = df[col].value_counts().head(5)
				for value, count in value_counts.items():
					text_parts.append(f"  {value}: {count}")
	
	return "\n".join(text_parts)


def load_file_to_text(filename: str, file_bytes: bytes) -> str:
	"""Return extracted text from an uploaded file based on extension."""
	lower = filename.lower()
	if lower.endswith(".txt"):
		return _read_txt(file_bytes)
	if lower.endswith(".docx"):
		return _read_docx(file_bytes)
	if lower.endswith(".pdf"):
		return _read_pdf(file_bytes)
	if lower.endswith(".csv"):
		return _read_csv(file_bytes)
	if lower.endswith((".xlsx", ".xls")):
		return _read_excel(file_bytes)
	raise ValueError(f"Unsupported file type: {filename}")

