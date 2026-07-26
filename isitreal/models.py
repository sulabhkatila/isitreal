from typing import Optional, List
from pydantic import BaseModel, Field


class PackageResult(BaseModel):
    """Result of a dependency existence and risk check."""

    name: str
    exists: bool
    canonical_name: Optional[str] = None
    latest_version: Optional[str] = None
    summary: Optional[str] = None
    first_release_date: Optional[str] = None
    total_releases: int = 0
    suggestions: List[str] = Field(default_factory=list)
    risk: Optional[str] = None  # "low", "unknown", "high", or None when exists=False
    reasons: List[str] = Field(default_factory=list)
    age_days: Optional[int] = None
