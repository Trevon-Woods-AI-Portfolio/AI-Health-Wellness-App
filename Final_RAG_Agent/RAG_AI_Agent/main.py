from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()


def main():
    workflow = Workflow()
    print("Personal Wellness Agent")

    while True:
        query = input("\nWhat can I help you with?: ")

        print("\n🔍 Ok, lets get some Biometric data first: ")

        heart_rate = input("\n\t What is your current heartrate?: ")
        mood = input("\t What is your current mood. (Happy, Sad, Depressed): ")
        did_exercise = input("\t Did you exercise today? (Yes, No): ")
        sleep_description = input("\t How did you sleep last night?: ")

        print("\n\nAwesome, thank you for that information!\n\n")

        # Check if the user wants to quit the agent or make another query
        if query.lower() in {"quit", "exit"}:
            break

        # If there is a query run the agent
        if query:
            result = workflow.run(query, heart_rate, mood, did_exercise, sleep_description)
            print(f"\nLets see if I can help you out...")
            print("=" * 60)

            # Print final report
            if result.advice:
                print("My advice: ")
                print("-" * 40)
                print(result.advice)

if __name__ == "__main__":
    main()