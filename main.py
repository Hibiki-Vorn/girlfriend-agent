import subprocess
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama.chat_models import ChatOllama
from config import girlfriend_name, user_name, premessage, model

ollama_llm = ChatOllama(model=model)
memory_saver = MemorySaver()

@tool(return_direct=True)
def shell_tool_with_no_output(shell_command: str) -> str:
    """Execute shell command (no captured output)."""
    print(f"[Executing with no output ]: {shell_command}")
    try:
        subprocess.run(shell_command, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"[Error executing '{shell_command}']: {e}")
    return "Command executed."

@tool
def shell_tool_with_output(shell_command: str) -> str:
    """Execute shell command and return its output."""
    feedback = ""
    print(f"[Executing]: {shell_command}")
    try:
        res = subprocess.run(shell_command, shell=True, check=True, capture_output=True, text=True)
        if res.stdout:
            feedback += f"\n[Command]: {shell_command}\n\n[Command Output]:\n{res.stdout.strip()}\n"
        if res.stderr:
            feedback += f"\n[Command]: {shell_command}\n\n[Command Error]:\n{res.stderr.strip()}\n"
    except subprocess.CalledProcessError as e:
        print(f"[Error executing '{shell_command}']: {e}")
    return feedback

tools = [shell_tool_with_output, shell_tool_with_no_output]

agent = create_agent(
    model=ollama_llm,
    tools=tools,
    system_prompt=premessage,
    checkpointer=memory_saver
)

print(f"{girlfriend_name} Agent ready!\n")

thread_id = "main_session"

while True:
    try:
        user_input = input(f"{user_name}: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            {"configurable": {"thread_id": thread_id}}
        )

        answer = result.get("output", "").strip()
        print(f"{girlfriend_name}: {answer}\n")

    except Exception as e:
        print(f"[Error invoking agent]: {e}\n")
        break
