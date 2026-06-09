#!/usr/bin/env python3
"""
Strategic Alignment Matrix Evaluator Agent.
Automates coordinate scoring and updates matrix_data.json based on debate verdicts.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBATES_DIR = os.path.join(BASE_DIR, "WORKSPACE", "simulation_arena", "debates")
MATRIX_JSON_PATH = os.path.join(BASE_DIR, "PROJECT_MANAGEMENT", "matrix_data.json")
EVALUATOR_PERSONA_PATH = os.path.join(BASE_DIR, "PLAYERS", "evaluator_persona.md")


def load_matrix_data():
    """Load existing matrix data JSON."""
    if os.path.exists(MATRIX_JSON_PATH):
        try:
            with open(MATRIX_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error reading matrix_data.json: {e}")
    return []


def save_matrix_data(data):
    """Save matrix data JSON."""
    try:
        with open(MATRIX_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving matrix_data.json: {e}")
        return False


def load_evaluator_persona():
    """Load the system persona guidelines."""
    try:
        with open(EVALUATOR_PERSONA_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"⚠️  Error reading evaluator_persona.md: {e}")
        return "You are the Strategic Matrix Evaluator."


class HeuristicEvaluator:
    """Heuristic positioning calculator for fallback/mock operations."""

    def evaluate(self, debate_json, debate_md_path):
        """Compute coordinates mathematically from debate verdict scores."""
        topic = debate_json["topic"]
        context = debate_json["context"]
        debate_id = debate_json["debate_id"]
        
        # Parse Arbitrator scores if available, else use defaults
        # We search inside the rounds or verdict
        verdict_text = debate_json.get("rounds", {}).get("round_3_verdict", "")
        
        # Heuristic scoring parser
        scores = {
            "strategic_value": 5,
            "technical_feasibility": 5,
            "market_timing": 5,
            "risk_profile": 5
        }
        
        # Try to extract scores from text
        for line in verdict_text.split("\n"):
            if "Strategic Value" in line and "|" in line:
                try:
                    parts = line.split("|")
                    scores["strategic_value"] = int(parts[2].strip())
                except: pass
            elif "Technical Feasibility" in line and "|" in line:
                try:
                    parts = line.split("|")
                    scores["technical_feasibility"] = int(parts[2].strip())
                except: pass
            elif "Market Timing" in line and "|" in line:
                try:
                    parts = line.split("|")
                    scores["market_timing"] = int(parts[2].strip())
                except: pass
            elif "Risk Profile" in line and "|" in line:
                try:
                    parts = line.split("|")
                    scores["risk_profile"] = int(parts[2].strip())
                except: pass

        # Composite score
        comp_score = round(sum(scores.values()) / len(scores), 1)

        # Coordinate calculations (Mapping to -100..100)
        # X-Axis (Maturity): derived from feasibility and timing
        x = (scores["technical_feasibility"] - 5) * 15 + (scores["market_timing"] - 5) * 10
        x = max(-100, min(100, x))

        # Y-Axis (Autonomy): derived from strategic value and risk profile (high risk = lower score, but high autonomy increases score)
        y = (scores["strategic_value"] - 5) * 20 - (scores["risk_profile"] - 5) * 8
        
        # Topic contextual shifts
        topic_lower = topic.lower()
        if "payment" in topic_lower or "fintech" in topic_lower or "wallet" in topic_lower:
            y += 25  # High autonomy required for payments
        if "browser" in topic_lower or "navigation" in topic_lower or "autonomous" in topic_lower:
            y += 20  # High autonomy required for navigation
        if "protocol" in topic_lower or "mcp" in topic_lower:
            y += 10
            
        y = max(-100, min(100, y))

        # Extract cleaner recommendation or verdict text
        verdict_desc = "Add to the strategic matrix as a debate-evaluated entity."
        for line in verdict_text.split("\n"):
            if "### Verdict" in line or "## Verdict" in line:
                # Get next non-empty line
                idx = verdict_text.find(line)
                sub = verdict_text[idx + len(line):].strip()
                if sub:
                    verdict_desc = sub.split("\n")[0].strip()
                break
            elif "Verdict" in line and len(line) > 15:
                verdict_desc = line.replace("### Verdict", "").replace("## Verdict", "").strip()

        if len(verdict_desc) > 200:
            verdict_desc = verdict_desc[:197] + "..."

        rel_md_path = os.path.relpath(debate_md_path, BASE_DIR)

        return {
            "name": topic,
            "x": int(x),
            "y": int(y),
            "category": "Debate-Evaluated",
            "desc": verdict_desc,
            "source": "debate",
            "composite_score": comp_score,
            "rationale": f"Strategic Value: {scores['strategic_value']}/10 | Technical Feasibility: {scores['technical_feasibility']}/10 | Market Timing: {scores['market_timing']}/10 | Risk Profile: {scores['risk_profile']}/10",
            "debate_id": debate_id,
            "report_anchor": rel_md_path,
            "scores": scores
        }


class OllamaEvaluator:
    """LLM positioning calculator using local Ollama instance."""

    def __init__(self, model="llama3.2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def evaluate(self, debate_json, debate_md_path):
        """Call Ollama chat API with evaluator guidelines and debate transcript."""
        persona = load_evaluator_persona()
        verdict_text = debate_json.get("rounds", {}).get("round_3_verdict", "")
        
        prompt = f"""Debate Topic: {debate_json['topic']}
Debate Context: {debate_json['context']}
Debate ID: {debate_json['debate_id']}
Markdown Report Location: {debate_md_path}

Arbitrator Consensus Verdict:
{verdict_text}

Analyze this verdict and output a JSON object positioning it on the Strategic Matrix.
"""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": persona},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json"
        }

        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read())
                content_str = result.get("message", {}).get("content", "{}")
                node_data = json.loads(content_str)
                
                # Ensure correct keys and relative path
                node_data["source"] = "debate"
                node_data["category"] = "Debate-Evaluated"
                node_data["debate_id"] = debate_json["debate_id"]
                node_data["report_anchor"] = os.path.relpath(debate_md_path, BASE_DIR)
                return node_data
        except Exception as e:
            print(f"⚠️  Ollama evaluation failed: {e}. Falling back to Heuristic calculation.")
            return HeuristicEvaluator().evaluate(debate_json, debate_md_path)


def process_debates(backend_type="mock"):
    """Scan and process completed debates, updating matrix_data.json."""
    if not os.path.exists(DEBATES_DIR):
        print(f"❌ Debates directory '{DEBATES_DIR}' does not exist.")
        return

    # Find all debate JSON files
    debate_files = [f for f in os.listdir(DEBATES_DIR) if f.endswith(".json") and f != "config.json"]
    if not debate_files:
        print("📭 No completed debates found to evaluate.")
        return

    matrix_nodes = load_matrix_data()
    evaluator = OllamaEvaluator() if backend_type == "ollama" else HeuristicEvaluator()

    updated_count = 0
    added_count = 0

    print(f"\n🧠 Evaluator Agent: Scanning {len(debate_files)} completed debates...")
    print("-" * 60)

    for fname in sorted(debate_files):
        json_path = os.path.join(DEBATES_DIR, fname)
        md_path = json_path.replace(".json", ".md")
        
        if not os.path.exists(md_path):
            continue

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                debate_data = json.load(f)
        except Exception as e:
            print(f"⚠️  Skipping '{fname}': error reading JSON ({e})")
            continue

        debate_id = debate_data.get("debate_id")
        if not debate_id:
            continue

        # Evaluate and calculate coordinates
        print(f"🔍 Analyzing Debate: '{debate_data['topic']}' ({debate_id})...")
        node = evaluator.evaluate(debate_data, md_path)

        # Check if already exists in matrix
        existing_idx = -1
        for idx, item in enumerate(matrix_nodes):
            if item.get("debate_id") == debate_id or (item.get("name") == node["name"] and item.get("source") == "debate"):
                existing_idx = idx
                break

        if existing_idx >= 0:
            # Update existing
            matrix_nodes[existing_idx] = node
            updated_count += 1
            print(f"  🔄 Updated Node: {node['name']} -> Coordinates (X: {node['x']}, Y: {node['y']})")
        else:
            # Append new
            matrix_nodes.append(node)
            added_count += 1
            print(f"  ✨ Added Node: {node['name']} -> Coordinates (X: {node['x']}, Y: {node['y']})")

    if updated_count > 0 or added_count > 0:
        if save_matrix_data(matrix_nodes):
            print("-" * 60)
            print(f"✅ Strategic Matrix update complete. Added: {added_count}, Updated: {updated_count} nodes.")
    else:
        print("-" * 60)
        print("ℹ️  No changes made. Matrix is already up-to-date.")


def main():
    parser = argparse.ArgumentParser(description="Strategic Matrix Positioning Automator")
    parser.add_argument("--backend", type=str, default="mock", choices=["mock", "ollama"],
                        help="Evaluation backend (mock/heuristic or ollama)")
    args = parser.parse_args()

    process_debates(args.backend)


if __name__ == "__main__":
    main()
