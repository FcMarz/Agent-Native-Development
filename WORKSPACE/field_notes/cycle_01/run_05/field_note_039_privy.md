# Privy: Self-Custodial Embedded Wallets for AI
> Ingested on: 2026-06-08 01:08:47
> Category: field_notes
> Index: 039
> Phase: 01 | Run: 05

# Profile
- **Name**: Privy
- **Category**: Embedded Onboarding & Wallet Security
- **Status**: Production-ready Web3 auth provider

# Agent-Native Characteristics
- **Shamir Secret Sharing (SSS)**: Secures agent keys by splitting them between the user's browser, Privy's HSM, and third-party storage.
- **Embedded Wallets**: Automatically provisions wallets for agents under OAuth authentication flows (e.g. signing in with Google or Discord).
- **Cross-App signing**: Permits agents to perform transactions across different dApps while keeping key shares locked in hardware enclaves.

# Aesthetic/UX Details
- Clean, customizable Web UI modals for user authentication and transaction confirmation prompts.

# Key Takeaways & Market Signal
- **Signal**: Self-custody must be simplified for agents. Distributing key shares across secure enclaves protects funds from single points of failure.
- **Reference**: https://www.privy.io