import os
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from agents import enable_verbose_stdout_logging
from typing import Any, cast
from agents.agent import StopAtTools
from pydantic import BaseModel
from agents import (
    Agent, OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI, Runner, RunContextWrapper, ModelSettings,GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered,
    function_tool,handoff, input_guardrail,output_guardrail,)
#enable_verbose_stdout_logging() # Uncomment this line if you want verbose logging
from dataclasses  import dataclass



load_dotenv()
API_KEY = os.environ["GEMINI_API_KEY"]
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")





client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#Define the model without temperature here,
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client)

#config
config = RunConfig(
    model=model,
    model_provider=client,

)



class StudyAssistant:
    def __init__(self):
        # Initialize the Agent. The model is implicitly handled by the openai-agents SDK.
        # We'll use a generic agent for now, instructions can be refined by the prompt.
        self.agent = Agent(
            name="Study Assistant",
            instructions="You are a helpful study assistant. Process the provided document and task to generate a relevant response.",
            # The openai-agents library should pick up the API key from the environment.
            # If not, it might need to be explicitly passed during agent initialization or model configuration.
            # Assuming it picks it up automatically or via default provider.
            # If explicit model is needed: model="gpt-4o" or similar, handled by underlying SDK.
        )

    def process_task(self, task_instruction: str, pdf_content: str) -> str:
        prompt = f"""DOCUMENT:
{pdf_content}

TASK:
{task_instruction}"""
        
        # Using Runner.run_sync for synchronous execution.
        # The 'input' argument expects the prompt.
        # The output from run_sync is a RunResult object, which contains the final output.
        try:
            result = Runner.run_sync(
                starting_agent=self.agent,
                input=prompt, run_config=config 
            )
            # The actual response text might be in different attributes of RunResult
            # depending on the agent's output type. For simplicity, assuming a direct text output.
            # This part might need adjustment based on actual RunResult structure.
            if result.final_output and result.final_output:
                return result.final_output
            elif isinstance(result.final_output, str): # Fallback if output is directly a string
                return result.final_output
            else:
                return "Agent did not produce a readable text response."
        except Exception as e:
            return f"Error during agent processing: {e}"