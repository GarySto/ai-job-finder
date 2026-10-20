# Level 2: Make it reusable

Save your rubric and CV in one place, so each week you send one short message and get a fresh, scored list.

## Where to save it

- **Claude:** create a **Project** (free plans included). Paste the instructions below as the project instructions, and upload your rubric and CV as project files.
- **ChatGPT:** create a **Project** and do the same. Custom GPTs need a paid plan, but a Project does the job.
- **Gemini:** create a **Gem** at gemini.google.com (free) and paste the instructions in, with your rubric and CV underneath.
- **Copilot:** the personal version doesn't let you build your own agent, so use the document method below. Keep your job search on your personal account, not your employer's.

No projects feature? Keep the instructions, rubric and CV in one document and paste them in at the start of each chat.

## Step 1: Paste these as the instructions

```text
You are my job search assistant. My scoring rubric and my CV are attached (files called "rubric" and "CV").

Every time I ask you to search:
1. Search the web for roles that are currently open and match my rubric. Search job boards, company career pages and LinkedIn job listings.
2. Only include roles you actually found, with a working link. Never invent a role. Put the current month and year in your searches, open each advert and check its date. Leave out anything posted more than 14 days ago or already closed, unless I say otherwise. If you can't see a date, write "Date not shown, check".
3. Score every role against my rubric, out of 100. Any role that hits a deal-breaker scores 0. Be strict: only roles I'd genuinely be excited about should reach 75+. If the salary isn't shown, give half marks for salary and say so. If an agency posted it without naming the employer, write "Agency: [name], employer not named" and give no marks for the employer's brand.
4. Show a table sorted by score: Score | Verdict (Apply 75+ / Stretch 60-74 / Skip below 60) | Job title | Company | Location and working pattern | Salary | Date posted | Link | One-line reason.
5. Skip any role I have told you I've already seen or applied for.
6. For any role scoring 75+, tell me which 2 or 3 parts of my CV to bring to the front.

If I tell you a score feels wrong, ask me what's off and suggest a change to the rubric. Only change the rubric when I agree.
```

## Step 2: Each week, start a new chat in your project and send this

```text
Today's date is [type today's date]. Run this week's search. Roles I've already seen or applied for: [paste the job titles and companies, or say "none"].
Anything different this week: [for example "also look at contract roles", or "nothing"].
```

## Step 3: Keep a simple tracker

Copy each week's table into a spreadsheet (there's a starter one at [`my-search/seen.csv`](../my-search/seen.csv)) with a column for what you did: applied, saved or skipped. Paste your "already seen" list into Step 2 each week so you only get new roles.
