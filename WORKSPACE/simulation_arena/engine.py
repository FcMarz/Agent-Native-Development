"""
Debate Engine — Core orchestrator for the Simulation Arena.
Manages the multi-round Bull/Bear/Arbitrator debate flow.
"""

import os
import json
import datetime


class DebateEngine:
    """Orchestrates a structured 3-round debate between Bull, Bear, and Arbitrator agents."""

    def __init__(self, backend, output_dir=None):
        self.backend = backend
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = output_dir or os.path.join(self.base_dir, "debates")
        os.makedirs(self.output_dir, exist_ok=True)

    def run_debate(self, topic, context, debate_id=None):
        """
        Execute a full 3-round debate on a given topic.
        
        Returns:
            dict: Complete debate transcript with metadata.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        debate_id = debate_id or f"debate_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        print(f"\n{'='*60}")
        print(f"🏟️  SIMULATION ARENA — Debate Session")
        print(f"{'='*60}")
        print(f"📋 Topic:   {topic}")
        print(f"🔧 Backend: {self.backend.name}")
        print(f"🕐 Time:    {timestamp}")
        print(f"{'='*60}\n")

        # === Round 1: Opening Statements ===
        print("📢 Round 1: Opening Statements")
        print("-" * 40)

        print("  🐂 Bull is preparing opening argument...")
        bull_opening = self.backend.generate_bull_opening(topic, context)
        print("  ✅ Bull opening complete.")

        print("  🐻 Bear is preparing opening argument...")
        bear_opening = self.backend.generate_bear_opening(topic, context)
        print("  ✅ Bear opening complete.")

        # === Round 2: Rebuttals ===
        print("\n📢 Round 2: Rebuttals")
        print("-" * 40)

        print("  🐂 Bull is reading Bear's argument and preparing rebuttal...")
        bull_rebuttal = self.backend.generate_bull_rebuttal(topic, bear_opening)
        print("  ✅ Bull rebuttal complete.")

        print("  🐻 Bear is reading Bull's argument and preparing rebuttal...")
        bear_rebuttal = self.backend.generate_bear_rebuttal(topic, bull_opening)
        print("  ✅ Bear rebuttal complete.")

        # === Round 3: Arbitrator Verdict ===
        print("\n📢 Round 3: Arbitrator Verdict")
        print("-" * 40)

        print("  ⚖️  Arbitrator is reviewing all arguments...")
        verdict = self.backend.generate_verdict(
            topic, context, bull_opening, bear_opening, bull_rebuttal, bear_rebuttal
        )
        print("  ✅ Verdict delivered.")

        # === Assemble Transcript ===
        transcript = {
            "debate_id": debate_id,
            "topic": topic,
            "context": context,
            "timestamp": timestamp,
            "backend": self.backend.name,
            "rounds": {
                "round_1_opening": {
                    "bull": bull_opening,
                    "bear": bear_opening
                },
                "round_2_rebuttal": {
                    "bull": bull_rebuttal,
                    "bear": bear_rebuttal
                },
                "round_3_verdict": verdict
            }
        }

        # === Save to disk ===
        md_path = self._save_transcript_md(transcript)
        json_path = self._save_transcript_json(transcript)

        print(f"\n{'='*60}")
        print(f"✅ Debate Complete!")
        print(f"  📄 Markdown: {md_path}")
        print(f"  📦 JSON:     {json_path}")
        print(f"{'='*60}\n")

        return transcript

    def _save_transcript_md(self, transcript):
        """Save the debate transcript as a formatted markdown file."""
        ts_slug = transcript["timestamp"].replace(" ", "_").replace(":", "-")
        topic_slug = transcript["topic"].lower().replace(" ", "_")[:40]
        filename = f"{ts_slug}_{topic_slug}.md"
        filepath = os.path.join(self.output_dir, filename)

        rounds = transcript["rounds"]

        content = f"""# 🏟️ Debate Transcript: {transcript['topic']}

> **Debate ID**: {transcript['debate_id']}
> **Date**: {transcript['timestamp']}
> **Backend**: {transcript['backend']}
> **Context**: {transcript['context']}

---

# Round 1: Opening Statements

{rounds['round_1_opening']['bull']}

---

{rounds['round_1_opening']['bear']}

---

# Round 2: Rebuttals

{rounds['round_2_rebuttal']['bull']}

---

{rounds['round_2_rebuttal']['bear']}

---

# Round 3: Verdict

{rounds['round_3_verdict']}
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def _save_transcript_json(self, transcript):
        """Save the debate transcript as structured JSON."""
        ts_slug = transcript["timestamp"].replace(" ", "_").replace(":", "-")
        topic_slug = transcript["topic"].lower().replace(" ", "_")[:40]
        filename = f"{ts_slug}_{topic_slug}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(transcript, f, indent=2, ensure_ascii=False)

        return filepath
