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


def load_file_to_text(filename: str, file_bytes: bytes) -> str:
	"""Return extracted text from an uploaded file based on extension."""
	lower = filename.lower()
	if lower.endswith(".txt"):
		return _read_txt(file_bytes)
	if lower.endswith(".docx"):
		return _read_docx(file_bytes)
	if lower.endswith(".pdf"):
		return _read_pdf(file_bytes)
	raise ValueError(f"Unsupported file type: {filename}")

