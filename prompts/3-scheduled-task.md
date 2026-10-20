# Level 3, route A: a scheduled task in your AI app

No code. You need an AI assistant that can run **scheduled tasks** (ChatGPT offers them on its paid plans and other assistants are adding similar features; look for "scheduled tasks" or "Tasks" in the app). Prefer something free and fully under your control? Use [route B, the GitHub version](../README.md#level-3-route-b-the-github-version).

1. Set up [Level 2](2-intermediate.md) first, so your rubric and CV are saved in a project.
2. Create a new scheduled task that runs once a week. Monday morning works well.
3. Paste the prompt below as the task's instructions.
4. If your assistant can connect to Google Drive or OneDrive, give it access to **one tracker spreadsheet only**. If it can't, it will send you the table and you copy it into your tracker.

```text
Weekly job sweep. Use my rubric and CV from my job search project.

1. Read my tracker spreadsheet (if you can access it) to see every role I've already seen. If you can't access it, use the list at the bottom of this message.
2. Search the web for roles posted in the last 7 days that match my rubric. Search job boards, company career pages and LinkedIn job listings, and put the current month and year in your searches.
3. Only include roles you actually found, with a working link. Never invent a role. Open each advert and check its date: leave out anything older than 7 days or already closed. Leave out any role already in my tracker.
4. Score each new role out of 100 against my rubric. Any role that hits a deal-breaker scores 0. Be strict. If the salary isn't shown, give half marks for salary and say so. If an agency posted it without naming the employer, say so and give no marks for the employer's brand.
5. If you can edit my tracker, add each new role as a new row: Date found | Score | Verdict | Job title | Company | Location | Salary | Link | Reason | Status (leave as "New"). Never delete or change existing rows.
6. Send me a short summary: how many new roles you found, then a table of only the roles scoring 60 or more, highest first. If nothing scored 60 or more, say so in one line. That's useful to know too.

Roles I've already seen (only needed if you can't read my tracker): [list]
```

**Keep it safe:** give the task access to the one tracker file it needs, never your whole drive or inbox. Never put passwords or job board logins in a prompt.
