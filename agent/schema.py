from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class MetaOut(BaseModel):
    domain_guess: Literal["logistics","fintech","healthcare","generic"]
    primary_actor: str
    affected_systems: List[str]

class ClarifyingQuestion(BaseModel):
    id: str
    type: Literal["scope","actor","data","edge_case","security","kpi","integration","acceptance"]
    text: str

class ClarifyOutput(BaseModel):
    meta: MetaOut
    questions: List[ClarifyingQuestion]

class Story(BaseModel):
    id: str = Field(pattern=r"US-\d{3}")
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: List[str]
    priority: Literal["Must","Should","Could"]
    dependencies: List[str] = []
    notes: Optional[str] = ""

class Epic(BaseModel):
    name: str
    description: str
    stories: List[Story]

class NFR(BaseModel):
    name: str
    requirement: str

class StoryOutput(BaseModel):
    epics: List[Epic]
    nfrs: List[NFR]
