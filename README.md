# Humans & AI : Public Site

The official public web face for **Humans & AI**.

[![Deploy with Vercel](https://vercel.com/button)](https://humans-and-ai.vercel.app)

---

## Identity & Mission

- **Author & Ownership:** Patrick McQueeny.
- **Mission:** Build and release sovereign, open-source software tools.
- **Architecture:** Zero-dependency static front end with HTML5, CSS3, and vanilla JS.
- **Design:** Deep Obsidian `#000000`, Pure White `#ffffff`, Electric Violet `#8a2be2`, Ina Violet `#8b5cf6`, Steel Grey `#808080`, Cascadia Code monospace typography.

---

## Public Repositories

The site covers six public open-source tools:

1. **[easylm.app](https://easylm.app)**: Sovereign in-browser WebGPU AI workstation with 30 collegiate textbooks, AtMem context governance, and zero remote cloud dependencies.
2. **[progen](https://github.com/erastudil/progen)**: Dialect of English applying Japanese topic-comment grammar for agent think traces, system prompts, and offline verification.
3. **[zcabs](https://github.com/erastudil/zcabs)**: Zero Context Agent Behavioral Scaffolding: deterministic proof-of-execution canary protocol and command-wrapping harness.
4. **[gfc](https://github.com/erastudil/gfc)**: Greene Feynman Clarity: writing standard and offline linter for human-facing prose.
5. **[hydra](https://github.com/erastudil/hydra)**: Sovereign multi-headed command-line AI engine, interactive TUI agent, and model gateway router with dual runtime parity in standard library Python and Node.
6. **[tankbench](https://github.com/erastudil/tankbench)**: Defensive hardening and security refactoring benchmark for autonomous coding agents.

---

## Local Verification & Development

```bash
# verify syntax, json-ld, and progen invariants:
python verify_site.py

# serve static site locally:
npx serve .
```

---

## Deployment

Pushes to the `main` branch trigger automatic production deployment via Vercel Git integration.

Manual production deployment via CLI:

```bash
npx vercel --prod
```