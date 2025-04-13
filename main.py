import argparse
import subprocess
import sys
import os

def run_agent(agent_name):
    """Runs the main script for the specified agent."""
    agent_dir_map = {
        "smol": "agent_smolagents",
        "llama": "agent_llamaindex",
        "graph": "agent_langgraph",
    }
    main_script_map = {
        "smol": "app.py",
        "llama": "app.py",
        "graph": "app.py",
    }

    if agent_name not in agent_dir_map:
        print(f"Error: Unknown agent '{agent_name}'. Choose from {list(agent_dir_map.keys())}")
        sys.exit(1)

    agent_dir = agent_dir_map[agent_name]
    main_script = main_script_map[agent_name]
    script_path = os.path.join(agent_dir, main_script)

    if not os.path.exists(script_path):
         print(f"Error: Main script not found at {script_path}")
         sys.exit(1)

    print(f"--- Running {agent_name} agent ---")
    # Use subprocess to run the script in its own directory context if needed
    # Or potentially import and call a main function if designed that way
    try:
        # Note: Running as subprocess ensures CWD is correct if scripts rely on relative paths
        process = subprocess.run([sys.executable, main_script], cwd=agent_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {agent_name} agent: {e}")
    except KeyboardInterrupt:
        print(f"\n--- {agent_name} agent interrupted ---")
    print(f"--- Finished {agent_name} agent ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run different agent implementations.")
    parser.add_argument("agent", choices=["smol", "llama", "graph"],
                        help="The name of the agent implementation to run.")
    # Add other potential arguments here if needed (e.g., input query)
    # parser.add_argument("-q", "--query", help="Input query for the agent")

    args = parser.parse_args()
    run_agent(args.agent)

