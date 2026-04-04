# PROMPT.md
# SSP-Project Prompts
# Team: Carter Williams, Sathvik Prahadeeswaran
# LLM: google/gemma-3-1b-it

---

## Zero-Shot

```
Please analyze the following two documents to identify key data elements: {file1} and {file2}. Structure your output as a nested dictionary with the following structure: {element1: {name: '', requirements: [req1, req2, req3]}, element2: {name: '', requirements: [req1, req2]} }
```

---

## Few-Shot

```
Please analyze the following two documents to identify key data elements: {file1} and {file2}. Structure your output as a nested dictionary with the following structure: {element1: {name: '', requirements: [req1, req2, req3]}, element2: {name: '', requirements: [req1, req2]} }. For example: element1: {name: 'title', requirements: ['human-readable', 'descriptive']} }. Also could be: element2: {name: 'rationale', requirements: ['sound reasoning', 'concise']}
```

---

## Chain-of-Thought

```
You are a thorough Cybersecurity Engineer. Please analyze the following two documents to identify key data elements: {file1} and {file2}. Structure your output as a nested dictionary with the following structure: {element1: {name: '', requirements: [req1, req2, req3]}, element2: {name: '', requirements: [req1, req2]} }. For example: element1: {name: 'title', requirements: ['human-readable', 'descriptive']} }. Also could be: element2: {name: 'rationale', requirements: ['sound reasoning', 'concise']}. Please think out loud as you go and detail your reasoning.
```
