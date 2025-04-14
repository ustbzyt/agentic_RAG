import argparse
import subprocess
import sys
import os
from typing import Dict, Optional

def run_agent(agent_name: str) -> None:
    """
    Runs the main script for the specified agent.
    
    Args:
        agent_name: Name of the agent to run (smol, llama, or graph)
    
    Raises:
        SystemExit: If agent_name is invalid or script is not found
    """
    agent_dir_map: Dict[str, str] = {
        "smol": "agent_smolagents",
        "llama": "agent_llamaindex",
        "graph": "agent_langgraph",
    }
    main_script_map: Dict[str, str] = {
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
    try:
        module_path = f"{agent_dir}.{main_script.replace('.py', '')}"     
        process = subprocess.run(
            [sys.executable, "-m", module_path],
            check=True,
            capture_output=False,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running {agent_name} agent: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n--- {agent_name} agent interrupted ---")
    print(f"--- Finished {agent_name} agent ---")

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Run different agent implementations.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "agent",
        choices=["smol", "llama", "graph"],
        help="The name of the agent implementation to run."
    )
    args = parser.parse_args()
    run_agent(args.agent)

if __name__ == "__main__":
    main()

