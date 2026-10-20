# AI Job Finder

**Free AI prompts and a template that help you find jobs that actually fit you.**

Instead of scrolling hundreds of adverts, you decide what a good role looks like *for you*, write it down as a scoring rubric, then let AI search the web and score every role it finds. You only spend time on the ones that score well.

I built this for my own job search and I'm sharing it because a lot of people I know have been made redundant from tech this year. The full walkthrough, with screenshots and tips, is on my site: **[How to use AI to find jobs that actually fit you](https://garystow.co.uk/guides/how-to-use-ai-to-find-jobs-that-fit-you/)**.

Pick the level that suits you:

| Level | What it is | You need | Time |
|---|---|---|---|
| [1. Starter](prompts/1-starter.md) | One copy-and-paste prompt. It interviews you, builds your rubric, reads your CV, searches and scores roles. | Any AI assistant with web search (free plans work) | About 20 minutes |
| [2. Intermediate](prompts/2-intermediate.md) | Save your rubric and CV in a project, then run a short search each week. | Claude, ChatGPT, Gemini or Copilot | 5 minutes a week |
| [3A. Scheduled task](prompts/3-scheduled-task.md) | Your AI app runs the search every week on its own. | An AI plan with scheduled tasks | Set up once |
| [3B. GitHub version](#level-3-route-b-the-github-version) | This repository. A free weekly GitHub Action that searches, scores, keeps a tracker and emails you a shortlist. | A free GitHub account and an Anthropic API key | Set up once, about 15 minutes |

> **Before you start:** remove your phone number, email address and home address from your CV. The AI doesn't need them.
> **And always check:** AI can get things wrong. Open the advert and check it before you apply.
>
> **Tested on:** Claude, Microsoft Copilot and Google Gemini (October 2026). ChatGPT not yet tested.

---

## How the rubric works

A rubric is a simple scorecard out of 100. You choose 4 to 6 sections that matter to you (the work itself, salary, location, whether you can meet the requirements, and so on) and give each one some points. Every role gets a score:

- **75 or more:** apply
- **60 to 74:** stretch, worth a closer look
- **Below 60:** skip
- **Hits a deal-breaker:** 0, whatever else it offers

There's an example in [`my-search/rubric.md`](my-search/rubric.md). The Level 1 prompt builds yours for you.

---

## Level 3, route B: the GitHub version

Every Monday morning, a GitHub Action reads your rubric and CV, asks Claude to search the web for roles posted that week, scores them, skips anything you've already seen, saves a report and opens an issue so GitHub emails you the shortlist.

**Cost:** GitHub Actions is free for this. You pay Anthropic for the API calls: a small amount per weekly run for the AI's reading and writing, plus web search, which is billed per search (this template caps it at 15 searches per run). Check [Anthropic's pricing page](https://www.anthropic.com/pricing) for current rates and set a monthly spending limit in the Anthropic Console so there are no surprises.

### Setup (about 15 minutes)

1. **Make your own private copy.** At the top of this page, click the green **Use this template** button, then **Create a new repository**. Give it a name, and choose **Private**. This matters, because your CV will live in it.
2. **Add your rubric.** In your new repository, open `my-search/rubric.md`, click the pencil icon (top right of the file) and replace the example with your own rubric. The easiest way to get one is to run the [Level 1 prompt](prompts/1-starter.md) and paste in the rubric it gives you at the end. Click **Commit changes**.
3. **Add your CV.** Open `my-search/cv.md`, click the pencil icon and paste your CV as plain text, without your contact details. Click **Commit changes**.
4. **Get an Anthropic API key.** Go to [console.anthropic.com](https://console.anthropic.com), sign up, add some credit under **Billing**, set a monthly limit, then go to **API keys** and click **Create key**. Copy the key. You'll only see it once.
5. **Add the key to your repository.** In your repository, click **Settings** (top menu), then **Secrets and variables → Actions** in the left menu, then **New repository secret**. Name: `ANTHROPIC_API_KEY`. Secret: paste your key. Click **Add secret**.
6. **Run it once to test.** Click the **Actions** tab, click **Weekly job search** on the left, then **Run workflow → Run workflow**. After a few minutes you'll get a new file in the `results` folder, a new issue with your shortlist, and an email from GitHub.

That's it. It now runs every Monday at 08:00 UK time (07:00 in winter).

### Changing how it works

You don't need to touch the code. Go to **Settings → Secrets and variables → Actions**, click the **Variables** tab, then **New repository variable**, and add any of these:

| Setting | Default | What it does |
|---|---|---|
| `MODEL` | `claude-sonnet-5-5` | Which Claude model runs the search |
| `MAX_SEARCHES` | `15` | Most web searches per run (caps the cost) |
| `DAYS_BACK` | `7` | How recent a role must be |
| `SHOW_FROM` | `60` | Lowest score that goes in your email |

To change the day or time, edit the `cron` line in `.github/workflows/weekly-search.yml`.

### Your tracker

Every new role, including the low scorers, is added to `my-search/seen.csv` with the status `New`, so you never see it twice. Download it and open it in Excel or Google Sheets, or edit the `status` column on GitHub (applied, saved, skipped) to keep track.

### Troubleshooting

- **The run fails with "cv.md still has the placeholder text"** or "rubric.md still has the example rubric": fill in those two files (steps 2 and 3).
- **"ANTHROPIC_API_KEY isn't set":** check the secret name is exactly `ANTHROPIC_API_KEY` (step 5).
- **A credit or billing error:** add credit in the Anthropic Console.
- **No email arrived:** check the **Issues** tab. If the issue is there, check your GitHub notification settings (your profile picture → **Settings → Notifications**).
- **The run fails at the "save" step:** go to **Settings → Actions → General → Workflow permissions** and choose **Read and write permissions**.

---

## Safety and privacy

- Keep your copy of this repository **private**.
- Never put contact details, passwords or job board logins in any file or prompt.
- Your API key lives only in GitHub Secrets. Never paste it into a file.
- Keep your job search on personal accounts, not work ones.

## Credit and licence

Made by [Gary Stow](https://garystow.co.uk). Free to use, copy and adapt under the [MIT licence](LICENSE). If it helps you land something, I'd love to hear about it on [LinkedIn](https://linkedin.com/in/garystow).
