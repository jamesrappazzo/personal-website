---
title: "Building Better LLM Evaluations"
date: 2026-01-08
draft: false
tags: ["ai", "llm", "evals", "engineering"]
categories: ["Engineering"]
description: "Lessons learned from building evaluation pipelines for agentic workflows"
---

## The Evaluation Problem

When you're building agentic workflows, one of the hardest challenges is knowing whether your system is actually getting better. Unlike traditional software where you can write deterministic tests, LLM outputs are inherently probabilistic.

I recently completed Hamel Husain's "AI Evals for Engineers & PMs" course, and it fundamentally changed how I approach evaluation. Here's what I learned.

## Start with Simple Assertions

Before you build complex eval frameworks, start with basic assertions:

```python
def test_agent_includes_sources():
    response = agent.run("What is the capital of France?")
    assert "Paris" in response
    assert len(response.sources) > 0
```

These won't catch everything, but they catch the obvious failures fast.

## Build a Golden Dataset

The most valuable thing you can do is build a high-quality golden dataset:

1. Collect real user queries (anonymized)
2. Manually write ideal responses for 50-100 examples
3. Version control this dataset
4. Run evals against it on every change

This becomes your regression test suite.

## LLM-as-Judge Works (With Constraints)

Using GPT-4 or Claude to evaluate other LLM outputs is controversial, but it works if you:

- Give it clear rubrics
- Use structured outputs (JSON scores)
- Spot check the evaluations yourself
- Never rely on it alone

I've found that combining LLM-as-judge with basic assertions gives you the best signal-to-noise ratio.

## What's Next

I'm working on open sourcing some of our evaluation infrastructure from my contracting work. Stay tuned for a deep dive on building eval pipelines with LangSmith.
