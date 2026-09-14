# Humans & AI — Public Site

The official public web face for **Humans & AI (HNAI)**.

[![Deploy with Vercel](https://vercel.com/button)](https://humans-and-ai.com)

---

## Identity & Brand Standards

- **Palette:** Deep Obsidian (`#07070a`), Pure White (`#ffffff`), Ina Violet (`#8b5cf6`), Steel Grey (`#71717a`).
- **Typography:** Cascadia Code / Inter Mono.
- **Architecture:** Zero-dependency static front end.
- **The Three Doors:**
  - **Door 1:** Free online browser intelligence and open education ([EasyLM](https://easylm.vercel.app)).
- **Field manual:** [defense against the dark arts](https://dadavol1.vercel.app) — cybersecurity hardening for AI-assisted solo developers (`dadavol1/`).
  - **Door 2:** Free open-source architectural skeletons, compilers, and specifications.
  - **Door 3:** Sovereign, owned installations and dedicated hardware appliances.

---

## Local Development

```bash
# Serve static site locally
npx serve .
```

---

## Deployment

Pushes to the `main` branch trigger automatic production deployment via Vercel Git integration.

Manual production deployment via CLI:

```bash
npx vercel --prod
```
