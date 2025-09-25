"""
run_pddl_up.py

This script automates the workflow of:
1. Loading a VirtualHome environment
2. Converting the environment graph into a PDDL problem
3. Saving the problem file
4. Loading and inspecting the PDDL problem using Unified Planning
5. Running a planner (Fast Downward via Unified Planning) to generate a plan
"""

import time
from virtualhome.simulation.unity_simulator import comm_unity
from project_code.environment_graph_to_pddl.automating_conversion_from_environment_graph import envgraph_to_pddl

# Unified Planning imports
from unified_planning.shortcuts import *
from unified_planning.io import PDDLReader
from unified_planning.engines import PlanGenerationResultStatus


def run_unified_planner(domain_file, problem_file):
    """
    Runs a planner from the Unified Planning library on the given domain and problem files.
    Returns the resulting plan as a list of actions.
    """
    reader = PDDLReader()
    problem = reader.parse_problem(domain_file, problem_file)

    # Choose a planner; "fast-downward" is supported if installed
    with OneshotPlanner(name="fast-downward") as planner:
        result = planner.solve(problem)

        if result.status == PlanGenerationResultStatus.SOLVED_SATISFICING:
            print("Planner finished. Plan found.")
            return [str(action) for action in result.plan.actions]
        else:
            print("Planner failed. Status:", result.status)
            return []


def inspect_problem(domain_file, problem_file):
    """
    Inspects the PDDL problem using Unified Planning,
    printing objects, initial state, and goals.
    """
    reader = PDDLReader()
    problem = reader.parse_problem(domain_file, problem_file)

    print("\nObjects in the problem:")
    for obj in problem.objects:
        print(f"{obj.name} : {obj.type}")

    print("\nInitial state fluents:")
    for f, v in problem.initial_values.items():
        print(f, "=", v)

    print("\nGoals:")
    for g in problem.goals:
        print(g)


def main():
    # =================== VirtualHome Setup ===================
    VIRTUALHOME_EXE = r"C:\Users\talsc\PycharmProjects\virtualhome_v1\virtualhome\simulation\unity_simulator\windows_exec\windows_exec.v2.3.0\VirtualHome.exe"
    PORT = "8080"

    # Initialize communication with VirtualHome
    comm = comm_unity.UnityCommunication(
        file_name=VIRTUALHOME_EXE,
        port=PORT
    )

    # =================== Load Environment ===================
    ENV_ID = 0
    comm.reset(ENV_ID)
    time.sleep(2)  # Give Unity time to load
    env_graph = comm.environment_graph()[1]

    # =================== Convert Environment Graph to PDDL ===================
    PDDL_PROBLEM_FILE = r"C:\Users\talsc\PycharmProjects\virtualhome\project_code\run_pddl\env1-problem.pddl"
    PDDL_DOMAIN_FILE = r"C:\Users\talsc\PycharmProjects\virtualhome\project_code\environment_graph_to_pddl\household-domain.pddl"

    # Convert the environment graph to a PDDL problem string
    pddl_problem_str = envgraph_to_pddl(env_graph, problem_name="env1_problem")

    # Save the problem to a file
    with open(PDDL_PROBLEM_FILE, "w") as f:
        f.write(pddl_problem_str)
    print(f"PDDL problem file saved to: {PDDL_PROBLEM_FILE}")

    # =================== Inspect the PDDL Problem ===================
    inspect_problem(PDDL_DOMAIN_FILE, PDDL_PROBLEM_FILE)

    # =================== Solve PDDL ===================
    plan = run_unified_planner(PDDL_DOMAIN_FILE, PDDL_PROBLEM_FILE)
    print("\nGenerated Plan:")
    for step in plan:
        print(step)


if __name__ == "__main__":
    main()
