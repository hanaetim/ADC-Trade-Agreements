"""Agent Registry Service - manages AGN1 (active) and AGN2-AGN6 (deferred) definitions."""
from dataclasses import dataclass


@dataclass
class AgentDefinition:
    """Agent definition for registry."""

    agent_id: str
    agent_name: str
    description: str
    executable_in_mvp: bool
    responsible_steps: list[str]


class AgentRegistryService:
    """Service managing agent registry (FR-002, FR-023, FR-024)."""

    # Static registry for MVP - in full implementation would read from agent_definitions table
    REGISTERED_AGENTS = [
        AgentDefinition(
            agent_id="AGN1",
            agent_name="Intake & Routing Agent",
            description="Executes ATS1-ATS3 intake workflow with deterministic validation",
            executable_in_mvp=True,
            responsible_steps=["ATS1", "ATS2", "ATS3"],
        ),
        AgentDefinition(
            agent_id="AGN2",
            agent_name="Request Comprehension Agent",
            description="Extracts structured facts from case evidence (deferred)",
            executable_in_mvp=False,
            responsible_steps=["ATS4"],
        ),
        AgentDefinition(
            agent_id="AGN3",
            agent_name="Origin Determination Agent",
            description="Applies agreement rules to produce origin determination (deferred)",
            executable_in_mvp=False,
            responsible_steps=["ATS5", "ATS6", "ATS7"],
        ),
        AgentDefinition(
            agent_id="AGN4",
            agent_name="Decision Drafting & Compliance Agent",
            description="Drafts decision package with compliance checks (deferred)",
            executable_in_mvp=False,
            responsible_steps=["ATS8", "ATS9"],
        ),
        AgentDefinition(
            agent_id="AGN5",
            agent_name="Approval & Issuance Agent",
            description="Routes for approval and handles issuance (deferred)",
            executable_in_mvp=False,
            responsible_steps=["ATS10", "ATS11", "ATS12", "ATS13"],
        ),
        AgentDefinition(
            agent_id="AGN6",
            agent_name="Dispute Adjudication Agent",
            description="Assists Technical Committee with dispute resolution (deferred)",
            executable_in_mvp=False,
            responsible_steps=["ATS14"],
        ),
    ]

    def get_active_agent(self, step_id: str) -> AgentDefinition | None:
        """Get executable agent for a step (only AGN1 in MVP)."""
        for agent in self.REGISTERED_AGENTS:
            if agent.executable_in_mvp and step_id in agent.responsible_steps:
                return agent
        return None

    def list_registered_agents(self) -> list[AgentDefinition]:
        """List all registered agents (AGN1-AGN6)."""
        return self.REGISTERED_AGENTS

    def get_agent_by_id(self, agent_id: str) -> AgentDefinition | None:
        """Get agent definition by ID."""
        for agent in self.REGISTERED_AGENTS:
            if agent.agent_id == agent_id:
                return agent
        return None
