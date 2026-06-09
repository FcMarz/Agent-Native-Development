#!/usr/bin/env python3
"""
Run Debate — CLI entry point for the Simulation Arena.

Usage:
    python3 run_debate.py                           # Run first pending topic from config
    python3 run_debate.py --topic "Skyfire"          # Run a specific topic
    python3 run_debate.py --backend ollama           # Use a different backend
    python3 run_debate.py --all                      # Run all pending topics
"""

import os
import sys
import json
import argparse

# Add parent paths for imports
ARENA_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ARENA_DIR)

from engine import DebateEngine
from backends.mock_backend import MockBackend


def load_config():
    """Load the arena configuration."""
    config_path = os.path.join(ARENA_DIR, "config.json")
    with open(config_path, "r") as f:
        return json.load(f)


def save_config(config):
    """Save the arena configuration."""
    config_path = os.path.join(ARENA_DIR, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_backend(backend_name):
    """Resolve a backend by name."""
    if backend_name == "mock":
        return MockBackend()
    elif backend_name == "ollama":
        try:
            from backends.ollama_backend import OllamaBackend
            return OllamaBackend()
        except ImportError:
            print("❌ Ollama backend not available. Falling back to mock.")
            return MockBackend()
    else:
        print(f"⚠️  Unknown backend '{backend_name}'. Using mock.")
        return MockBackend()


def main():
    parser = argparse.ArgumentParser(description="🏟️ Simulation Arena — Run a structured debate")
    parser.add_argument("--topic", type=str, help="Specific topic to debate")
    parser.add_argument("--backend", type=str, default=None, help="Backend to use (mock, ollama)")
    parser.add_argument("--all", action="store_true", help="Run all pending debate topics")
    args = parser.parse_args()

    config = load_config()
    backend_name = args.backend or config.get("default_backend", "mock")
    backend = get_backend(backend_name)
    engine = DebateEngine(backend)

    if args.topic:
        # Find topic in config or create ad-hoc
        topic_entry = None
        for t in config["topics"]:
            if args.topic.lower() in t["title"].lower():
                topic_entry = t
                break

        if not topic_entry:
            # Create ad-hoc topic
            topic_entry = {
                "id": f"debate-adhoc",
                "title": args.topic,
                "context": f"User-specified topic: {args.topic}",
                "status": "pending"
            }

        transcript = engine.run_debate(
            topic=topic_entry["title"],
            context=topic_entry["context"],
            debate_id=topic_entry["id"]
        )

        # Mark as completed in config
        for t in config["topics"]:
            if t.get("id") == topic_entry.get("id"):
                t["status"] = "completed"
        save_config(config)

    elif args.all:
        pending = [t for t in config["topics"] if t["status"] == "pending"]
        if not pending:
            print("📭 No pending debate topics found.")
            return

        print(f"🏟️  Running {len(pending)} pending debates...\n")
        for topic_entry in pending:
            engine.run_debate(
                topic=topic_entry["title"],
                context=topic_entry["context"],
                debate_id=topic_entry["id"]
            )
            topic_entry["status"] = "completed"
            save_config(config)

    else:
        # Run first pending topic
        pending = [t for t in config["topics"] if t["status"] == "pending"]
        if not pending:
            print("📭 No pending debate topics. Add new topics to config.json or use --topic.")
            return

        topic_entry = pending[0]
        engine.run_debate(
            topic=topic_entry["title"],
            context=topic_entry["context"],
            debate_id=topic_entry["id"]
        )
        topic_entry["status"] = "completed"
        save_config(config)


if __name__ == "__main__":
    main()
