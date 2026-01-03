from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool, input_guardrail, GuardrailFunctionOutput
from typing import Dict
import sendgrid
from openai import OpenAI
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
import asyncio
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from pydantic import BaseModel

load_dotenv(override=True)

gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

if not os.environ.get("SENDGRID_API_KEY"):
    raise RuntimeError("SENDGRID_API_KEY not set")

from_base_email = os.getenv('FROM_EMAIL')
to_base_email = os.getenv('TO_EMAIL')


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=gemini_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash-lite", openai_client=gemini_client)

instructions1 = "You are a sales agent working for QuestAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for QuestAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for QuestAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."

class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

guardrail_agent = Agent( 
    name="Name check",
    instructions="Check if the user is including someone's personal name in what they want you to do.",
    output_type=NameCheckOutput,
    model="gpt-4o-mini"
)

@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered=is_name_in_message)

@function_tool
def send_email(body: str):
    """ Send out an email with the given body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_base_email)  # Change to your verified sender
    to_email = To(to_base_email)  # Change to your recipient
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, "Sales email", content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

sales_agent1 = Agent(
        name="Professional Sales Agent",
        instructions=instructions1,
        model=gemini_model,
)

sales_agent2 = Agent(
        name="Engaging Sales Agent",
        instructions=instructions2,
        model=gemini_model,
)

sales_agent3 = Agent(
        name="Busy Sales Agent",
        instructions=instructions3,
        model=gemini_model,
)

description = "Write a cold sales email"

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

tools = [tool1, tool2, tool3, send_email]


instructions = """
You are a Sales Manager at QuestAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
 
3. Use the send_email tool to send the best email (and only the best email) to the user.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must send ONE email using the send_email tool — never more than one.
"""


sales_manager = Agent(
    name="Sales Manager",
    instructions=instructions,
    tools=tools,
    model=gemini_model,
    input_guardrails=[guardrail_against_name]
)

message = "Send a cold sales email addressed to 'Dear CEO'"

async def main():
        
        result = await Runner.run(sales_manager, message)
    

asyncio.run(main())
