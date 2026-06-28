"""
Description: The Data Schemes or Pydantic Data Models. Enforces predictable schemas over unstructured LLM extractions using Pydantic.
Author: Sudeep Varma K
Date: 2026-06-27
"""
from pydantic import BaseModel
class PolicySummary(BaseModel):
    title: str
    effective_date: str
    billing_codes: list[str]
    prerequisites: list[str]
    penalties: list[str]
    summary: str