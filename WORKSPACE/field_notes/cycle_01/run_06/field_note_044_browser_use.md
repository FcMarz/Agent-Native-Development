# browser-use: Open-Source LLM Browser Automation Driver
> Ingested on: 2026-06-08 01:22:21
> Category: field_notes
> Index: 044
> Phase: 01 | Run: 06

# Profile
- **Name**: browser-use
- **Category**: Vision-Based Web Agent Driver
- **Status**: Rapidly growing open-source python framework

# Agent-Native Characteristics
- **DOM-to-Action Mapping**: Converts Chrome DOM trees and visual screenshots into click/type/scroll coordinates for the LLM.
- **Self-Correcting Navigation**: Automatically checks page states and retries actions if the page fails to load or shows captcha roadblocks.
- **Multi-Tab Execution**: Coordinates complex visual operations across multiple tabs in real time.

# Aesthetic/UX Details
- Renders a live browser window highlighting agent actions, element tags, and step-by-step reasoning streams.

# Key Takeaways & Market Signal
- **Signal**: Visual web drivers are replacing fragile Selenium/Playwright scripts. Agents that parse pages like humans (by looking and pointing) are resilient to website restyling.
- **Reference**: https://github.com/browser-use/browser-use