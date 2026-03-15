"""Multi-agent system implementation."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass
import anthropic
import os


@dataclass
class AgentResponse:
    """Response from an agent."""
    agent_name: str
    output: str
    confidence: float
    metadata: Dict[str, Any]


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        """Execute the agent's task."""
        pass
    
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM with a prompt."""
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class ResearchAgent(BaseAgent):
    """Agent for research tasks."""
    
    def __init__(self):
        super().__init__("ResearchAgent")
    
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        prompt = f"""You are a research specialist. Research the following topic thoroughly:

Task: {task}
Context: {context}

Provide a comprehensive summary with key findings, relevant facts, and sources.
"""
        output = self._call_llm(prompt)
        
        return AgentResponse(
            agent_name=self.name,
            output=output,
            confidence=0.85,
            metadata={"sources_checked": 5}
        )


class CodeAgent(BaseAgent):
    """Agent for code generation and review."""
    
    def __init__(self):
        super().__init__("CodeAgent")
    
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        prompt = f"""You are an expert software engineer. Generate production-quality code:

Task: {task}
Context: {context}

Requirements:
- Write clean, well-documented code
- Include error handling
- Follow best practices
- Add type hints where appropriate

Provide the code and a brief explanation.
"""
        output = self._call_llm(prompt)
        
        return AgentResponse(
            agent_name=self.name,
            output=output,
            confidence=0.90,
            metadata={"language": context.get("language", "python")}
        )


class ValidationAgent(BaseAgent):
    """Agent for validating outputs."""
    
    def __init__(self):
        super().__init__("ValidationAgent")
    
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        output_to_validate = context.get("output_to_validate", "")
        
        prompt = f"""You are a validation specialist. Review the following output for correctness:

Original Task: {task}
Output to Validate:
{output_to_validate}

Check for:
1. Factual accuracy
2. Logical consistency
3. Completeness
4. Potential errors

Provide a validation report with issues found (if any) and overall assessment.
"""
        output = self._call_llm(prompt)
        
        # Extract confidence from validation
        confidence = 0.95 if "no issues" in output.lower() else 0.70
        
        return AgentResponse(
            agent_name=self.name,
            output=output,
            confidence=confidence,
            metadata={"validation_passed": confidence > 0.80}
        )


class SecurityAgent(BaseAgent):
    """Agent for security review."""
    
    def __init__(self):
        super().__init__("SecurityAgent")
    
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        code_to_review = context.get("code", "")
        
        prompt = f"""You are a security expert. Review the following for security vulnerabilities:

Context: {task}
Code/Content to Review:
{code_to_review}

Check for:
1. Injection vulnerabilities
2. Authentication/authorization issues
3. Data exposure risks
4. Input validation
5. Secrets management

Provide a security assessment with severity ratings for any issues found.
"""
        output = self._call_llm(prompt)
        
        # Lower confidence if security issues found
        has_issues = "vulnerability" in output.lower() or "risk" in output.lower()
        confidence = 0.60 if has_issues else 0.95
        
        return AgentResponse(
            agent_name=self.name,
            output=output,
            confidence=confidence,
            metadata={"security_clearance": not has_issues}
        )


class AgentOrchestrator:
    """Orchestrates multiple agents to complete tasks."""
    
    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "code": CodeAgent(),
            "validation": ValidationAgent(),
            "security": SecurityAgent(),
        }
    
    async def execute_single_agent(
        self,
        agent_name: str,
        task: str,
        context: Dict[str, Any]
    ) -> AgentResponse:
        """Execute a single agent."""
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        return await agent.execute(task, context)
    
    async def execute_collaborative(
        self,
        task: str,
        agents: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute multiple agents and aggregate results."""
        import asyncio
        
        # Execute all agents in parallel
        tasks = [
            self.execute_single_agent(agent_name, task, context)
            for agent_name in agents
        ]
        responses = await asyncio.gather(*tasks)
        
        # Aggregate results
        results = {
            "task": task,
            "agent_responses": {},
            "consensus_score": 0.0,
            "final_output": "",
            "requires_human_review": False
        }
        
        total_confidence = 0
        for response in responses:
            results["agent_responses"][response.agent_name] = {
                "output": response.output,
                "confidence": response.confidence,
                "metadata": response.metadata
            }
            total_confidence += response.confidence
        
        # Calculate consensus
        results["consensus_score"] = total_confidence / len(responses) if responses else 0
        
        # Require human review if consensus is low
        if results["consensus_score"] < 0.75:
            results["requires_human_review"] = True
        
        # Generate final output (would use LLM to synthesize in production)
        results["final_output"] = self._synthesize_outputs(responses)
        
        return results
    
    def _synthesize_outputs(self, responses: List[AgentResponse]) -> str:
        """Synthesize multiple agent outputs into a final result."""
        # Simple concatenation for demo - in production, use LLM to synthesize
        outputs = [f"## {r.agent_name}\n{r.output}\n" for r in responses]
        return "\n---\n".join(outputs)


if __name__ == "__main__":
    import asyncio
    
    async def main():
        orchestrator = AgentOrchestrator()
        
        # Example: Multi-agent code generation
        result = await orchestrator.execute_collaborative(
            task="Create a secure Python API endpoint for customer data",
            agents=["code", "validation", "security"],
            context={"framework": "FastAPI", "database": "PostgreSQL"}
        )
        
        print(f"Consensus Score: {result['consensus_score']}")
        print(f"Requires Human Review: {result['requires_human_review']}")
        print("\nFinal Output:")
        print(result['final_output'])
    
    asyncio.run(main())
