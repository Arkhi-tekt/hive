# 🇿🇲 Lusaka Website Scout

This is your first "AI Employee" tailored for the Lusaka business market. It finds local businesses, audits their websites for design flaws, and reports the best leads for your Web Development and Graphics services.

## 🛠️ What it does:
1.  **Discovery**: Searches Google for businesses in Lusaka based on a category you provide (e.g., "Law firms" or "Schools").
2.  **Audit**: Visits their websites and looks for "Red Flags" like:
    *   Outdated designs.
    *   No mobile support.
    *   Old copyright dates.
3.  **Report**: Gives you a list of businesses that desperately need a redesign, along with a "Sales Pitch" for each one.

## 🚀 How to use it:

### Option A: The Dashboard (Easiest)
1.  Run `./hive tui` in your terminal.
2.  Find **Lusaka Website Scout** in the list.
3.  Input a category (like "Dentists in Lusaka") and watch it work!

### Option B: Command Line
From the project root, run:
```bash
uv run python -m examples.templates.lusaka_website_scout --category "Law firms in Lusaka"
```

## 📂 Files:
- `agent.json`: The "Map" of how the agent thinks.
- `agent.py`: The "Brain" that runs the nodes.
- `nodes/`: The specific steps (Search, Audit, Report).
