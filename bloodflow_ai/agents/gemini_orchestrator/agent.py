"""
Gemini Orchestrator

LLM-powered orchestrator that uses Gemini to decide which tools to call.
This is a wrapper around the existing agents that adds LLM reasoning.
"""

import json
import re
from typing import Optional, Dict, Any, List

from bloodflow_ai.agents.emergency_triage.agent import EmergencyTriageAgent
from bloodflow_ai.agents.donor_matching.agent import DonorMatchingAgent
from bloodflow_ai.agents.communication.agent import CommunicationAgent
from bloodflow_ai.schemas.response_schema import WorkflowResponse
from bloodflow_ai.schemas.request_schema import HospitalRequest
from bloodflow_ai.tools.llm_tools import LLMTools
from bloodflow_ai.memory.store import MemoryStore, InMemoryStore


class GeminiOrchestrator:
    """
    LLM-powered Orchestrator that uses Gemini for reasoning.

    How it works:
    1. User provides raw input
    2. Emergency Triage Agent parses it → HospitalRequest
    3. Gemini decides which tools to call based on the request
    4. Tools are executed sequentially
    5. Results are returned
    """

    def __init__(
        self,
        memory_store: Optional[MemoryStore] = None,
        use_gemini: bool = True
    ):
        self.memory_store = memory_store or InMemoryStore()
        self.triage = EmergencyTriageAgent()
        self.matcher = DonorMatchingAgent()
        self.communicator = CommunicationAgent(memory_store=self.memory_store)
        self.use_gemini = use_gemini

    def run(self, raw_input: str) -> WorkflowResponse:
        """
        Execute the workflow with LLM reasoning.

        Args:
            raw_input: Unstructured text from hospital

        Returns:
            WorkflowResponse with status and details
        """
        print("\n" + "=" * 60)
        print("[Gemini Orchestrator] 🧠 Starting LLM-powered workflow...")
        print("=" * 60)
        print(f"[Gemini Orchestrator] Input: {raw_input}")

        # Step 1: Always use Emergency Triage (deterministic)
        structured_request = self.triage.process(raw_input)

        if not structured_request:
            return WorkflowResponse(
                status="failed",
                message="Failed to parse hospital request",
                donor_contacted=None,
                donors_considered=0
            )

        print(f"[Gemini Orchestrator] ✅ Triage: {structured_request.blood_group} @ {structured_request.hospital}")

        if self.use_gemini:
            # Step 2: Let Gemini decide which tools to call
            return self._run_with_gemini(structured_request)
        else:
            # Fallback to deterministic logic
            return self._run_deterministic(structured_request)

    def _run_with_gemini(self, request: HospitalRequest) -> WorkflowResponse:
        """Run the workflow using Gemini tool calling."""
        try:
            # pyrefly: ignore [missing-import]
            from google import genai
        except ImportError:
            print("[Gemini Orchestrator] ⚠️ Gemini SDK not installed. Falling back to deterministic mode.")
            return self._run_deterministic(request)

        # Get donors for context
        donors = self.matcher.match(request, max_results=10)

        if not donors:
            print("[Gemini Orchestrator] ❌ No donors found")
            return WorkflowResponse(
                status="failed",
                message="No donors found",
                donor_contacted=None,
                donors_considered=0
            )

        # Create LLM tools WITH DONORS
        llm_tools = LLMTools(donors)

        # Build the system prompt
        system_prompt = self._build_system_prompt(request, donors)

        try:
            # Call Gemini with tool definitions
            client = genai.Client()

            # Get Gemini's plan
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=system_prompt,
                config={
                    "temperature": 0.2,
                    "max_output_tokens": 1024,
                }
            )

            # Parse Gemini's decision
            plan = response.text

            print(f"[Gemini Orchestrator] 🧠 Gemini Plan:\n{plan}")

            # Execute the plan
            result = self._execute_plan(plan, llm_tools, request, donors)

            return result

        except Exception as e:
            print(f"[Gemini Orchestrator] ❌ Error: {e}")
            print("[Gemini Orchestrator] ⚠️ Falling back to deterministic mode.")
            return self._run_deterministic(request)

    def _build_system_prompt(self, request: HospitalRequest, donors: List) -> str:
        """Build the system prompt for Gemini."""
        donor_summary = []
        for i, donor in enumerate(donors[:5], 1):
            donor_summary.append(
                f"{i}. {donor.name} ({donor.blood_group}): age={donor.age}, location={donor.location}, "
                f"response_rate={donor.response_rate}, available={donor.available}"
            )

        prompt = f"""
You are the Orchestrator for BloodFlow AI, a blood donation coordination system.

## Current Situation
- Hospital Request: {request.blood_group} blood needed
- Hospital: {request.hospital}
- Urgency: {request.urgency}
- Units Needed: {request.units}
- Deadline: {request.deadline}

## Available Donors (Top 5)
{chr(10).join(donor_summary)}

## Available Tools
1. `find_nearest_donors(blood_group, location, limit)` - Find donors by blood group and location
2. `check_availability(donor_id)` - Check if a donor is available and eligible
3. `rank_donors(donors)` - Rank a list of donors by score
4. `notify_donor(donor_id, message)` - Notify a donor
5. `ask_rag(question)` - Ask a question about blood donation guidelines (WHO, eligibility)

## Task
Create a plan to find and notify a suitable donor.

## Output Format
Return ONLY valid JSON with:
1. "reasoning": Brief explanation of your strategy
2. "steps": List of tool calls to execute

Example:
{{
    "reasoning": "I will find nearby O- donors, check availability, rank them, and notify the best one.",
    "steps": [
        {{"tool": "find_nearest_donors", "args": {{"blood_group": "O-", "location": "Dhaka", "limit": 10}}}},
        {{"tool": "check_availability", "args": {{"donor_id": 1}}}},
        {{"tool": "rank_donors", "args": {{"donors": []}}}},
        {{"tool": "notify_donor", "args": {{"donor_id": 1, "message": "Emergency blood needed"}}}}
    ]
}}

Now create your plan. Return ONLY the JSON, no markdown.
"""
        return prompt

    def _clean_plan(self, plan_text: str) -> Dict[str, Any]:
        """
        Clean Gemini's response and extract JSON.

        Handles:
        - Markdown code blocks (```json ... ```)
        - Extra whitespace
        - Partial JSON extraction
        """
        # Remove markdown code blocks
        plan_text = re.sub(r'```json\s*', '', plan_text)
        plan_text = re.sub(r'```\s*', '', plan_text)
        plan_text = plan_text.strip()

        # Try to find JSON object
        json_match = re.search(r'\{.*\}', plan_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError as e:
                print(f"[Gemini Orchestrator] ⚠️ JSON decode error: {e}")

        # If no JSON found, try to extract from text
        try:
            # Try parsing the whole thing
            return json.loads(plan_text)
        except json.JSONDecodeError:
            pass

        return {"steps": [], "reasoning": "Could not parse Gemini response"}

    def _execute_plan(self, plan: str, llm_tools: LLMTools, request: HospitalRequest, donors: List) -> WorkflowResponse:
        """Execute the plan generated by Gemini."""
        try:
            # Clean and parse the plan
            plan_data = self._clean_plan(plan)
            steps = plan_data.get("steps", [])
            reasoning = plan_data.get("reasoning", "")

            if not steps:
                print("[Gemini Orchestrator] ⚠️ No steps in plan. Using deterministic fallback.")
                return self._run_deterministic(request)

            print(f"[Gemini Orchestrator] 📋 Executing {len(steps)} steps...")
            print(f"[Gemini Orchestrator] 🧠 Reasoning: {reasoning}")

            # Execute each step
            for step in steps:
                tool_name = step.get("tool")
                args = step.get("args", {})

                print(f"[Gemini Orchestrator] 🔧 Calling {tool_name} with {args}")

                if tool_name == "find_nearest_donors":
                    result = llm_tools.find_nearest_donors(**args)
                elif tool_name == "ask_rag":
                    result = llm_tools.ask_rag(**args)
                elif tool_name == "check_availability":
                    result = llm_tools.check_availability(**args)
                elif tool_name == "rank_donors":
                    result = llm_tools.rank_donors(args.get("donors", []))
                elif tool_name == "notify_donor":
                    result = llm_tools.notify_donor(**args)
                elif tool_name == "get_donor_details":
                    result = llm_tools.get_donor_details(**args)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                # If a donor was notified, check if they accepted
                if tool_name == "notify_donor" and result.get("status") == "accepted":
                    return WorkflowResponse(
                        status="success",
                        message=f"Donor {result.get('donor')} accepted",
                        donor_contacted=result.get("donor"),
                        request=request.model_dump(),
                        donors_considered=len(donors)
                    )

            # If no donor accepted, fallback to deterministic
            print("[Gemini Orchestrator] ⚠️ No donor accepted via Gemini plan. Using deterministic fallback.")
            return self._run_deterministic(request)

        except Exception as e:
            print(f"[Gemini Orchestrator] ❌ Error executing plan: {e}")
            print("[Gemini Orchestrator] ⚠️ Falling back to deterministic mode.")
            return self._run_deterministic(request)

    def _run_deterministic(self, request: HospitalRequest) -> WorkflowResponse:
        """Fallback to deterministic workflow."""
        print("[Gemini Orchestrator] 🔄 Using deterministic workflow.")

        donors = self.matcher.match(request, max_results=5)

        if not donors:
            return WorkflowResponse(
                status="failed",
                message="No donors found",
                donor_contacted=None,
                donors_considered=0
            )

        comm_result = self.communicator.notify(request, donors)

        return WorkflowResponse(
            status=comm_result.status,
            message=comm_result.message,
            donor_contacted=comm_result.accepted_donor,
            request=request.model_dump(),
            donors_considered=comm_result.attempts
        )