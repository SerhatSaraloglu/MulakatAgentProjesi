from app.agents import interview_agent
from app.interview_agent import __doc__ as legacy_doc


def test_interview_agent_module_has_project_placeholder():
    assert "Interview orchestration placeholder" in interview_agent.__doc__


def test_legacy_agent_module_marks_new_source_of_truth():
    assert "app/agents/interview_agent.py" in legacy_doc
