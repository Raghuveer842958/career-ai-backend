# from ai.rag.ingest import ingest_resume

from ai.agent.agent import get_career_agent

RESUME_PATH = "ai/data/Raghuveer_Resume.pdf"

# ingest_resume(RESUME_PATH)

agent = get_career_agent()

while True:

    query = input("\nAsk Something : ")

    response = agent.invoke({
        "input": query
    })

    print("\nAI Response:\n")

    print(response["output"])

    # TOKEN DATA
    steps = response.get("intermediate_steps", [])

    if steps:
        try:
            usage = steps[0][0].message_log[0].usage_metadata
            print("\n===== TOKEN USAGE =====")
            print(f"Input Tokens: {usage['input_tokens']}")
            print(f"Output Tokens: {usage['output_tokens']}")
            print(f"Total Tokens: {usage['total_tokens']}")
        except Exception:
            print("Token metadata not available in this step.")
    else:
        print("\nNo tool execution → no intermediate steps.")
