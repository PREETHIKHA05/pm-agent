import json
from agent.schema import StoryOutput, ClarifyOutput

def test_story_schema_example():
    data = {
        "epics":[{"name":"Proof of Delivery","description":"...","stories":[
            {"id":"US-001","as_a":"Ops Agent","i_want":"verify PoD","so_that":"confirm delivery",
             "acceptance_criteria":["Given X When Y Then Z"],"priority":"Must","dependencies":[],"notes":""}
        ]}],
        "nfrs":[{"name":"Security","requirement":"Encrypt at rest"}]
    }
    StoryOutput.model_validate(data)

def test_clarify_schema_example():
    data = {
        "meta":{"domain_guess":"logistics","primary_actor":"Ops Agent","affected_systems":["Mobile","Backoffice"]},
        "questions":[
            {"id":"Q1","type":"scope","text":"Is signature only or include photos?"},
            {"id":"Q2","type":"actor","text":"Who approves PoD?"},
            {"id":"Q3","type":"data","text":"What metadata to capture?"},
            {"id":"Q4","type":"edge_case","text":"How to handle network loss?"},
            {"id":"Q5","type":"security","text":"Any PII restrictions?"},
            {"id":"Q6","type":"kpi","text":"Target verification SLA?"},
            {"id":"Q7","type":"integration","text":"Systems to integrate?"},
            {"id":"Q8","type":"acceptance","text":"Acceptance criteria baseline?"}
        ]
    }
    ClarifyOutput.model_validate(data)
