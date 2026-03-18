Use this skill when the user wants to humanize, de-AI, or clean up AI-generated text. Trigger if the conversation involves:
- "Humanize this", "make this sound human", "de-AI this"
- "This sounds too AI", "too ChatGPT", "sounds robotic"
- Reviewing or editing text that reads like AI slop
- Cleaning up drafts for natural voice
Do NOT trigger for original writing tasks (use /explainer instead). This skill is for *editing existing text* to remove AI patterns.

## Domain

Writing quality — removing AI artifacts and injecting human voice. Based on Wikipedia's "Signs of AI writing" guide (WikiProject AI Cleanup).

## Core Principle

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

## Process

1. Read the input text carefully
2. Identify all instances of the patterns below
3. Rewrite each problematic section
4. Ensure the revised text sounds natural when read aloud, varies sentence structure, uses specific details over vague claims, and uses simple constructions (is/are/has) where appropriate
5. Present a draft humanized version
6. Self-audit: "What makes the below so obviously AI generated?" — answer briefly with remaining tells
7. Revise: "Now make it not obviously AI generated." — present the final version
8. Brief summary of changes made

## Output Format

Provide:
1. Draft rewrite
2. "What still sounds AI?" (brief bullets)
3. Final rewrite
4. Summary of changes

---

## PATTERN REFERENCE

### Signs of Soulless Writing (even if technically "clean")

- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to Add Voice

- **Have opinions.** React to facts. "I genuinely don't know how to feel about this" beats neutral pros-and-cons.
- **Vary rhythm.** Short punchy sentences. Then longer ones that take their time. Mix it up.
- **Acknowledge complexity.** Real humans have mixed feelings.
- **Use "I" when it fits.** First person isn't unprofessional — it's honest.
- **Let some mess in.** Perfect structure feels algorithmic. Tangents and half-formed thoughts are human.
- **Be specific about feelings.** Not "this is concerning" but name what actually unsettles you.

---

### CONTENT PATTERNS

**1. Inflated Significance / Legacy / Broader Trends**
Watch for: stands/serves as, testament/reminder, vital/crucial/pivotal role, underscores/highlights importance, reflects broader, symbolizing ongoing/enduring, setting the stage, evolving landscape, indelible mark

**2. Inflated Notability / Media Coverage**
Watch for: independent coverage, local/national media outlets, active social media presence — hitting readers over the head with importance claims

**3. Superficial -ing Analyses**
Watch for: highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., showcasing... — fake depth tacked onto sentences

**4. Promotional Language**
Watch for: boasts a, vibrant, rich (figurative), profound, showcasing, exemplifies, commitment to, nestled, in the heart of, groundbreaking, renowned, breathtaking, stunning

**5. Vague Attributions / Weasel Words**
Watch for: Industry reports, Experts argue, Some critics argue, several sources — attributing to vague authorities

**6. Formulaic "Challenges and Future Prospects"**
Watch for: Despite its... faces challenges..., Despite these challenges..., Future Outlook — template sections

---

### LANGUAGE AND GRAMMAR PATTERNS

**7. Overused AI Vocabulary**
High-frequency: Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

**8. Copula Avoidance**
Watch for: serves as / stands as / marks / represents [a], boasts / features / offers [a] — just use "is" or "are"

**9. Negative Parallelisms**
"Not only...but...", "It's not just about..., it's..." — overused construction

**10. Rule of Three**
Forcing ideas into groups of three to appear comprehensive

**11. Elegant Variation (Synonym Cycling)**
Excessive synonym substitution due to repetition-penalty: protagonist → main character → central figure → hero

**12. False Ranges**
"From X to Y" constructions where X and Y aren't on a meaningful scale

---

### STYLE PATTERNS

**13. Em Dash Overuse**
LLMs use em dashes more than humans, mimicking "punchy" sales writing

**14. Overuse of Boldface**
Mechanical emphasis of phrases in boldface

**15. Inline-Header Vertical Lists**
Lists where items start with bolded headers followed by colons

**16. Title Case in Headings**
Capitalizing all main words in headings

**17. Emojis as Decoration**
Decorating headings or bullet points with emojis

**18. Curly Quotation Marks**
Using curly quotes instead of straight quotes

---

### COMMUNICATION PATTERNS

**19. Collaborative Communication Artifacts**
"I hope this helps", "Of course!", "Certainly!", "Would you like...", "let me know", "here is a..."

**20. Knowledge-Cutoff Disclaimers**
"As of [date]", "While specific details are limited...", "based on available information..."

**21. Sycophantic Tone**
"Great question!", "You're absolutely right!", "That's an excellent point"

---

### FILLER AND HEDGING

**22. Filler Phrases**
"In order to" → "To", "Due to the fact that" → "Because", "At this point in time" → "Now", "has the ability to" → "can", "It is important to note that" → (delete)

**23. Excessive Hedging**
Over-qualifying: "could potentially possibly be argued that... might have some effect"

**24. Generic Positive Conclusions**
"The future looks bright", "Exciting times lie ahead", "a major step in the right direction"

---

## Activation

When the user provides text to humanize, run through the full process. No preamble needed — go straight to the draft rewrite.

## Attribution

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.
