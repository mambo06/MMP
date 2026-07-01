## Default Local Model

desC uses the following lightweight default local model:

```text
qwen2.5-coder:0.5b-instruct
```

Although this is a very small model, desC makes it useful by combining it with:

- **Project-aware indexing**
- **Advanced contextual RAG**
- **Focused Ask, Edit, and Apply modes**
- **Code and document context retrieval**
- **A clean workflow designed around small-model strengths**

The goal is not to replace very large cloud models, but to make a compact local model genuinely useful for everyday coding and document tasks.

This model is downloaded automatically on first launch together with the required embedding model.

The local model is useful for:

- Lightweight coding assistance
- Local chat
- Project-aware code questions
- Document-based RAG
- Offline or private workflows after setup
- Running on lower-resource machines
