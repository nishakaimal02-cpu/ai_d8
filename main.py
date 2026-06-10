from crewai import Crew, Process
from dotenv import load_dotenv
from agents import coverage_analyst, pricing_optimizer, merchant_comms, manager_agent
from tasks import coverage_analysis_task, pricing_optimization_task, merchant_comms_task
import os

load_dotenv()

def run_sequential_crew():
    print("\n" + "="*60)
    print("RUNNING CREW IN SEQUENTIAL MODE")
    print("="*60 + "\n")

    crew = Crew(
        agents=[coverage_analyst, pricing_optimizer, merchant_comms],
        tasks=[coverage_analysis_task, pricing_optimization_task, merchant_comms_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    
    print("\n" + "="*60)
    print("FINAL CREW OUTPUT — SEQUENTIAL")
    print("="*60)
    print(result)
    
    output_path = "/Users/nishakshitij/Desktop/AI Builds/ai_d8/output_hierarchical.txt"
    with open(output_path, "w") as f:
        f.write(str(result))
    print(f"\nOutput saved to {output_path}")
    return result


def run_hierarchical_crew():
    print("\n" + "="*60)
    print("RUNNING CREW IN HIERARCHICAL MODE")
    print("="*60 + "\n")

    crew = Crew(
        agents=[coverage_analyst, pricing_optimizer, merchant_comms],
        tasks=[coverage_analysis_task, pricing_optimization_task, merchant_comms_task],
        process=Process.hierarchical,
        manager_llm="gpt-4o",
        manager_agent=manager_agent,
        verbose=True,
        max_iter=15
    )

    result = crew.kickoff()
    
    print("\n" + "="*60)
    print("FINAL CREW OUTPUT — HIERARCHICAL")
    print("="*60)
    print(result)
    
    output_path = "/Users/nishakshitij/Desktop/AI Builds/ai_d8/output_hierarchical.txt"
    with open(output_path, "w") as f:
        f.write(str(result))
    print(f"\nOutput saved to {output_path}")
    return result


if __name__ == "__main__":
    print("Which mode do you want to run?")
    print("1 — Sequential")
    print("2 — Hierarchical")
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        run_sequential_crew()
    elif choice == "2":
        run_hierarchical_crew()
    else:
        print("Invalid choice. Running sequential by default.")
        run_sequential_crew()