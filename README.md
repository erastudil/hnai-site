# Humans & AI — Public Site

The official public web face for **Humans & AI (HNAI)**.

[![Deploy with Vercel](https://vercel.com/button)](https://humans-and-ai.vercel.app)

---

## Identity & Mission

- **Author & Ownership:** Patrick McQueeny (owned as a human being; zero corporate shield).
- **Mission:** Build sovereign open-source software, collaborate with educators and students, live on donations.
- **Palette:** Deep Obsidian (`#07070a`), Pure White (`#ffffff`), Ina Violet (`#8b5cf6`), Steel Grey (`#71717a`).
- **Typography:** Cascadia Code / Monospace.
- **Architecture:** Zero-dependency static front end.
- **Key Links:**
  - **EasyLM:** Sovereign in-browser WebGPU AI with 28 Dewey collegiate textbooks ([easylm.app](https://easylm.app)).
  - **Field Manual:** Defense Against the Dark Arts ([dadavol1.vercel.app](https://dadavol1.vercel.app) · local `dadavol1/`).
  - **GitHub:** Open source repositories and tools ([github.com/erastudil](https://github.com/erastudil)).

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
