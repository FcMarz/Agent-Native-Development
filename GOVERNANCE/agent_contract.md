# Governance Contract: Human-Agent Collaboration

This document defines the rules of engagement, permissions, and operating guidelines for the autonomous research agent in this workspace.

---

## 🔒 Boundaries and Permissions

1. **Human-Only Zone (`GOVERNANCE/`)**:
   - The agent is forbidden from editing any files in the `GOVERNANCE/` folder unless explicitly directed by the human user.
   - Any proposed changes to the rules of engagement must be reviewed and approved by the human in the chat.
2. **Execution Permissions**:
   - The agent is pre-authorized to run read-only shell commands, query folder listings, edit research documents, and execute server helpers.
   - **Destructive operations** (e.g. deleting folders, resetting git state, or modifying host system settings outside the workspace) require explicit human approval.

---

## 📝 Document and Archiving Conventions

1. **Structured Research Loop**:
   - The agent writes individual findings to `WORKSPACE/field_notes/field_note_XXX.md`.
   - Every **8 field notes**, the agent synthesizes findings into an **Interim Insight Report** in `ARCHIVE/interim/`.
   - Every **8 interim reports** (totaling 64 field notes), the agent compiles a **Final Report** in `ARCHIVE/final/` featuring an executive summary and a proposed plan for the next research run.
2. **Changelog & Session logs**:
   - The agent records every major execution step and file write in `LOGS/session_diary.md`.
   - Each diary entry records the datetime, action taken, path written, and current git commit hash.

---

## 🛠️ Git as Source of Truth

1. **Automatic Commits**:
   - Every paste or write action will trigger an automatic git commit.
   - Commit messages must follow the pattern: `ingest(category): add [Document Title]`.
2. **Workspace Cleanliness**:
   - The workspace must remain structured. Scraping caches or raw JSON downloads belong in `WORKSPACE/raw_data/` and must not clutter the root.
