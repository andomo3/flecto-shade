---
name: hackathon-prompts
description: Write prompts for AI coding tools during a hackathon using the HackMIT playbook - the CTCF framework (Context, Task, Constraints, Format), the prompt quality ladder from bad to great, the 50 hackathon specific prompts across code generation, UI, API integration, debugging, documentation, and pitch writing, the common prompt mistakes, the tool specific tips for Cursor, Copilot, Claude, v0, and Bolt, the manual coding survival guide for when AI fails, and the 3 AM exhaustion templates. Use this whenever the user is drafting a prompt for Cursor, Copilot, Claude, v0, Bolt, or any AI assistant, asks why the AI output is bad or generic, wants a reusable prompt template, mentions hallucinated code, or is exhausted and needs the AI to carry more of the load. Built from the AI Prompt Engineering section of the playbook.
---

# Hackathon prompts

The teams winning are not always the best coders.
They are the ones who know how to talk to AI: a good prompt turns a two hour feature into fifteen minutes, and a vague one produces vague code with edge cases that crash on stage.
This skill writes the prompt so the first output is the one that runs.

| Need | Read |
|---|---|
| The CTCF framework, the 50 prompts by category, the quality ladder, the failure modes and the manual emergency kit, tool tips, the common mistakes, the 3 AM framework, the quick reference card | `references/ai-prompts.md` |

## Every prompt has four parts

**Context.** The project, the stack with versions, what is already built.
The tool does not remember the last conversation.

**Task.** Exactly what is needed.
"Build a login page" is weak; "a React login form with email and password, validation, error states, and a submit handler that calls `/api/auth`" is strong.

**Constraints.** Stack, design system, performance, accessibility, existing patterns to follow.
Constraints force relevant answers instead of generic ones.

**Format.** Single file or several, comments or not, a step by step or the code.

Write the prompt in that order, label the parts, and lead with the stack, because the AI will otherwise pick one.

## Climb the ladder before sending

The reference shows bad, good, and great versions for six kinds of prompt.
The pattern is the same each time: the great version names the library, lists the states (loading, error, empty), gives the exact endpoint and data shape, names the file to match, and says what to include.
When a draft prompt reads like the "good" rung, add the states, the shapes, and the file to match, and it becomes the "great" one.

For a task the playbook has already written, start from the matching prompt among the fifty in the reference: ten for code generation, ten for UI components, eight for API integration, eight for debugging, seven for documentation, seven for pitch and script writing.
Adapt the brackets rather than writing from a blank page.

## The mistakes that waste hours

Being vague ("make it look good"), no context (a bug with no code or error), too much at once ("build my entire app"), accepting the first output untested, ignoring existing code, forgetting edge cases, not naming the stack, and accepting hallucinated code.
The fixes are one line each: be specific to the pixel, paste the error and the code and the expectation, one prompt per component or endpoint, generate then test then refine three times, point at the file to imitate, ask for loading and error and empty states, lead with the stack, run every function immediately.

## When AI fails

It hallucinates APIs, suggests deprecated patterns, writes circular logic, over engineers, and loses context after five prompts.
Survival moves from the reference: keep the official docs open and test every call, check the changelog, draw the call graph, ask for "the simplest version with no abstractions", and restate the architecture in one prompt before asking for new code.
When it fails completely: copy from the docs, use a template generator, take the top Stack Overflow answer, use the browser's built in features, or switch to another model.

## Tool tips

- **Cursor.** `@codebase` for project wide context, a `.cursorrules` file with the conventions, inline edits for small changes, agent mode for multi file work.
- **Copilot.** Write the comment first and let it complete; use chat for complex questions.
- **Claude.** Paste whole files, use projects for continuity, ask for trade-offs before code, use it for review.
- **v0.** Describe the component visually and reference a real product.
- **Bolt.** Be extremely specific about the stack in the first prompt and include the schema.

## At 3 AM

The tired brain cannot hold context, so write it all down using the exhaustion template: project, exact tech versions, current state, the single thing needed now, the error if any.
Keep the UI, API, and debug templates from the reference saved in notes.
When too tired to write a prompt, ask the AI to explain the code back first, then ask for the change.
When nothing works, paste the whole file and the line number.
And if the bugs being chased do not exist, a twenty minute nap with an alarm finds more of them than another hour awake.
