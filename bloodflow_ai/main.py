from bloodflow_ai.agents.orchestrator.agent import Orchestrator


def main():
    orchestrator = Orchestrator()

    request = input("Enter hospital request: ")

    result = orchestrator.run(request)

    print("\n\n===== FINAL OUTPUT =====")
    print(result)


if __name__ == "__main__":
    main()
