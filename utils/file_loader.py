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
	
	# Convert DataFrame to a readable text format
	text_parts = []
	
	# Add column names
	text_parts.append("Columns: " + ", ".join(df.columns.tolist()))
	text_parts.append("")
	
	# Add data summary
	text_parts.append(f"Data Summary:")
	text_parts.append(f"- Total rows: {len(df)}")
	text_parts.append(f"- Total columns: {len(df.columns)}")
	text_parts.append("")
	
	# Add first few rows as sample data
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
	raise ValueError(f"Unsupported file type: {filename}")

