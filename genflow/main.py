
from modules.agents.orchestrator import AgentOrchestrator

if __name__ == "__main__":
    orchestrator = AgentOrchestrator("genflow\\tasks\\example_task.yaml")
    orchestrator.run()
