from typing import List, Optional
from pydantic import BaseModel


class ResearchIdea(BaseModel):
    title: str
    rationale: str
    method_outline: str
    novelty_score: int
    feasibility_score: int


class SectionItems(BaseModel):
    items: List[str]


class NewKnowledgeAndFindings(BaseModel):
    empirical_evidence: SectionItems
    novel_findings: SectionItems
    theoretical_contributions: SectionItems


class DeeperUnderstanding(BaseModel):
    contextualization: SectionItems
    critical_analysis: SectionItems
    implications: SectionItems


class GapsAndLimitations(BaseModel):
    knowledge_gaps: SectionItems
    limitations_of_previous_studies: SectionItems
    future_research_directions: SectionItems


class PracticalApplications(BaseModel):
    real_world_applications: SectionItems
    informing_decision_making: SectionItems
    developing_new_technologies: SectionItems


class AnalysisResult(BaseModel):
    summary: str
    new_knowledge_and_findings: NewKnowledgeAndFindings
    deeper_understanding_and_interpretation: DeeperUnderstanding
    identification_of_gaps_and_limitations: GapsAndLimitations
    practical_applications_and_recommendations: PracticalApplications
    research_ideas: List[ResearchIdea]
    citations_note: Optional[str] = None


class AnalyzeResponse(BaseModel):
    ok: bool
    result: AnalysisResult


class ErrorResponse(BaseModel):
    ok: bool
    error: str