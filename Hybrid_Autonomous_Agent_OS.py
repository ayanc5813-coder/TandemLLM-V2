# Generated from: Hybrid_Autonomous_Agent_OS.ipynb
# Converted at: 2026-05-29T23:45:09.651Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

!pip -q install langgraph langchain langchain-community langchain-core
!pip -q install transformers accelerate bitsandbytes sentence-transformers
!pip -q install chromadb gradio
!pip -q install litellm

import os
import json
import chromadb
import gradio as gr

from typing import TypedDict

from transformers import pipeline

from langgraph.graph import StateGraph, END

from litellm import completion

os.environ["OPENROUTER_API_KEY"] = "YOUR_API_KEY"

!pip install -q transformers accelerate sentencepiece

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

import chromadb

client = chromadb.Client()

try:
    memory_collection = client.get_collection("agent_memory")

except:
    memory_collection = client.create_collection("agent_memory")

def save_memory(user_input, response):

    short_response = response[:1000]

    memory_collection.add(
        documents=[
            f"USER: {user_input[:500]}\nAI: {short_response}"
        ],
        ids=[str(hash(user_input + short_response))]
    )


def retrieve_memory(query, n=1):

    try:

        results = memory_collection.query(
            query_texts=[query[:500]],
            n_results=n
        )

        docs = results["documents"][0]

        compressed_docs = []

        for d in docs:
            compressed_docs.append(d[:1000])

        return compressed_docs

    except:
        return []

def cloud_llm(prompt):

    response = completion(
        model="openrouter/openai/gpt-oss-120b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["choices"][0]["message"]["content"]

def local_llm(prompt):

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=64,
        temperature=0.7
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return response

#print(local_llm(
#    "Summarize AI in 3 bullet points"
#))

def router_agent(user_input):

    text = user_input.lower()

    # SIMPLE / FAST TASKS → LOCAL

    local_keywords = [

        "grammar",
        "correct",
        "fix sentence",
        "short summary",
        "summarize",
        "translate",
        "regex",
        "simple python",
        "small code",
        "email",
        "bullet points",
        "reverse string",
        "hello world"
    ]

    # COMPLEX TASKS → CLOUD

    cloud_keywords = [

        "recipe",
        "research",
        "startup",
        "business",
        "architecture",
        "design",
        "roadmap",
        "strategy",
        "analyze",
        "comparison",
        "travel",
        "plan",
        "healthcare",
        "finance",
        "investment",
        "multi-agent",
        "system design",
        "deployment",
        "production",
        "detailed",
        "features"
    ]

    # LOCAL FIRST

    for word in local_keywords:
        if word in text:
            return "local"

    # CLOUD NEXT

    for word in cloud_keywords:
        if word in text:
            return "cloud"

    # LENGTH-BASED FALLBACK

    if len(text) < 80:
        return "local"

    return "cloud"

def planner_agent(user_input):

    planning_prompt = f"""
    Break the following task into step-by-step subtasks.

    TASK:
    {user_input}

    Return concise numbered steps.
    """

    return cloud_llm(planning_prompt)

def tool_agent(user_input):

    if "python" in user_input.lower():
        return "Python tool suggested"

    if "search" in user_input.lower():
        return "Web search suggested"

    return "No external tool needed"

def verifier_agent(user_input, output):

    verification_prompt = f"""
    Evaluate this AI response.

    USER TASK:
    {user_input}

    AI OUTPUT:
    {output}

    Return ONLY:

    PASS

    or

    FAIL
    """

    verdict = cloud_llm(verification_prompt)

    return "PASS" in verdict.upper()

def repair_agent(user_input, failed_output):

    repair_prompt = f"""
    The following response failed verification.

    USER TASK:
    {user_input}

    FAILED OUTPUT:
    {failed_output}

    Improve and repair the answer.
    """

    return cloud_llm(repair_prompt)

class AgentState(TypedDict):
    user_input: str
    route: str
    plan: str
    tool_info: str
    output: str
    verified: bool

def routing_node(state):

    route = router_agent(state["user_input"])

    return {
        "route": route
    }



def planning_node(state):

    plan = planner_agent(state["user_input"])

    return {
        "plan": plan
    }



def tool_node(state):

    tool_info = tool_agent(state["user_input"])

    return {
        "tool_info": tool_info
    }



def execution_node(state):

    short_task = state["user_input"][:1000]

    short_plan = state["plan"][:1000]

    prompt = f"""
    TASK:
    {short_task}

    PLAN:
    {short_plan}
    """

    if state["route"] == "local":
        output = local_llm(prompt)
    else:
        output = cloud_llm(prompt)

    return {
        "output": output
    }



def verification_node(state):

    verified = verifier_agent(
        state["user_input"],
        state["output"]
    )

    return {
        "verified": verified
    }



def repair_node(state):

    repaired = repair_agent(
        state["user_input"],
        state["output"]
    )

    return {
        "output": repaired,
        "verified": True
    }

workflow = StateGraph(AgentState)

workflow.add_node("router", routing_node)
workflow.add_node("planner", planning_node)
workflow.add_node("tool", tool_node)
workflow.add_node("execute", execution_node)
workflow.add_node("verify", verification_node)
workflow.add_node("repair", repair_node)

workflow.set_entry_point("router")

workflow.add_edge("router", "planner")
workflow.add_edge("planner", "tool")
workflow.add_edge("tool", "execute")
workflow.add_edge("execute", "verify")


def verification_router(state):

    if state["verified"]:
        return END

    return "repair"


workflow.add_conditional_edges(
    "verify",
    verification_router
)

workflow.add_edge("repair", END)

app = workflow.compile()

def run_hybrid_system(user_input):

    memory = retrieve_memory(user_input)

    state = {
        "user_input": f"""
        MEMORY:
        {memory}

        CURRENT TASK:
        {user_input}
        """
    }

    result = app.invoke(state)

    final_output = result["output"]

    save_memory(user_input, final_output)

    return final_output

#response = run_hybrid_system(
#   "Research AI startup ideas in healthcare and create execution roadmap"
#)

print(response)

def get_route_badge(route):

    if route == "cloud":
        return "☁️ Cloud Agent Used"

    return "💻 Local Device Agent Used"

def run_hybrid_system_ui(user_input):

    route = router_agent(user_input)

    # FAST LOCAL PATH

    if route == "local":

        response = local_llm(user_input)

        return (
            "💻 FAST LOCAL DEVICE AGENT",
            "Skipped planner for speed",
            "No tools needed",
            response
        )

    # SLOW CLOUD PATH

    memory = retrieve_memory(user_input)

    state = {
        "user_input": f"""
        MEMORY:
        {memory}

        CURRENT TASK:
        {user_input}
        """
    }

    result = app.invoke(state)

    final_output = result["output"]

    plan = result["plan"]

    tool_info = result["tool_info"]

    save_memory(user_input, final_output)

    return (
        "☁️ ADVANCED CLOUD AGENT SYSTEM",
        plan,
        tool_info,
        final_output
    )

with gr.Blocks() as demo:

    gr.Markdown(
        "# Hybrid Autonomous Agent OS"
    )

    gr.Markdown(
        "Cloud + Device Hybrid Multi-Agent System"
    )

    user_input = gr.Textbox(
        lines=6,
        label="User Task",
        placeholder="Ask anything..."
    )

    run_button = gr.Button("Run Hybrid Agent System")

    route_output = gr.Textbox(
        label="Execution Route"
    )

    plan_output = gr.Textbox(
        lines=8,
        label="Planner Agent Output"
    )

    tool_output = gr.Textbox(
        lines=3,
        label="Tool Agent Output"
    )

    final_output = gr.Textbox(
        lines=15,
        label="Final AI Response"
    )

    run_button.click(
        fn=run_hybrid_system_ui,
        inputs=user_input,
        outputs=[
            route_output,
            plan_output,
            tool_output,
            final_output
        ]
    )


demo.launch(share=True)
