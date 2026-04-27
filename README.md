# ✈️ GitHub Copilot Demo

> *"With great AI comes great responsibility."* — Uncle Ben, probably, if he worked in tech.

Welcome to **copilot-demo-02** — a Streamlit web app so impressive it makes Iron Man's JARVIS look like a pocket calculator. This project is your interactive tour guide through the top superpowers of [GitHub Copilot](https://github.com/features/copilot), built entirely with Python and a healthy dose of caffeine.

---

## 🚀 What Is This Thing?

Think of this app as the Hogwarts Express, except instead of taking you to wizarding school, it takes you on a tour of AI-powered coding wizardry. Three stops on the journey:

| Page | What it does |
|------|-------------|
| 🏠 **Home** | Showcases the top 10 GitHub Copilot features in slick animated cards. It's basically the "Previously on GitHub Copilot…" recap you never knew you needed. |
| 🧮 **Calculator** | A sleek node-style calculator. Does it solve differential equations? No. Does it look cool doing basic arithmetic? Absolutely. |
| 💡 **Code Generation Lab** | Six stub functions sit here, staring blankly like NPCs waiting for a quest. Fire up GitHub Copilot, delete those `pass` statements, and watch magic happen live. |

---

## 🛠️ Tech Stack

This app is built on the shoulders of giants — or at least the shoulders of very good open-source maintainers:

- **[Python 3.13+](https://www.python.org/)** — the language that's basically English for computers
- **[Streamlit ≥ 1.30](https://streamlit.io/)** — turns Python scripts into web apps faster than you can say "React boilerplate"
- **[Bootstrap 5](https://getbootstrap.com/)** — making things look pretty since the Dark Ages (circa 2013)
- **[Bootstrap Icons](https://icons.getbootstrap.com/)** — tiny pictures worth a thousand words

---

## ⚡ Getting Started

> *"Every journey begins with a single `pip install`."* — Confucius (updated edition)

### Prerequisites

- Python 3.13 or higher (older versions will be judged silently)
- `pip` (or a time machine to a world where package managers don't exist)

### Installation

```bash
# 1. Clone this repo like you mean it
git clone https://github.com/ajafry/copilot-demo-02.git
cd copilot-demo-02

# 2. (Optional but wise) Create a virtual environment
#    "To venv or not to venv" — there is no question
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies — one small pip for man, one giant leap for your project
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

Your browser will open automatically. If it doesn't, navigate to `http://localhost:8501` — Streamlit's version of Platform 9¾.

---

## 🗺️ Project Structure

```
copilot-demo-02/
├── app.py                  # The One Ring that rules them all (entry point + routing)
├── requirements.txt        # Dependency scroll — ingredients for our magic potion
└── views/
    ├── __init__.py         # Python's "nothing to see here" file
    ├── home.py             # Top-10 Copilot features showcase
    ├── calculator.py       # Four operations, infinite style
    ├── codegen_lab.py      # Six stubs waiting for Copilot to save the day
    └── styles.py           # CSS sorcery — Bootstrap injected straight into the veins
```

---

## 💡 Code Generation Lab: How to Play

1. Open `views/codegen_lab.py` in VS Code (or your editor of choice — we don't judge, but VS Code has Copilot integration so… choose wisely).
2. Find one of the six functions with a `pass` body:
   - `reverse_string` — Yoda-speak generator, essentially
   - `is_palindrome` — "Was it a car or a cat I saw?"
   - `fizzbuzz` — the rite of passage of every junior dev interview
   - `celsius_to_fahrenheit` — for the one country still using Fahrenheit
   - `count_vowels` — surprisingly useful, inexplicably satisfying
   - `find_max` — finding the biggest number without `max()`, like opening a jar without the lid
3. Delete `pass`, place your cursor, and invoke GitHub Copilot (`Ctrl+I` / `Cmd+I`).
4. Accept the suggestion, refresh the Streamlit app, and bask in glory.

---

## 🤖 About GitHub Copilot

GitHub Copilot is the AI pair-programmer that never gets tired, never asks for a coffee break, and never judges you for writing `# TODO: fix this later` at 2 AM. Powered by large language models, it offers:

- **Real-time code completions** as you type
- **Natural language chat** in your editor
- **Test generation**, **documentation generation**, and **PR code reviews**
- **Multi-language support** across Python, JavaScript, TypeScript, Java, Go, C#, and many more
- **Agent Mode** — let Copilot plan *and* implement multi-step tasks while you supervise (and take credit in stand-up)

---

## 🧑‍💻 Contributing

Contributions are welcome! Whether you're fixing a typo, adding a feature, or dramatically over-engineering the calculator — all PRs will be reviewed by at least one human (and possibly also by Copilot, the circle of life).

1. Fork the repo
2. Create a branch: `git checkout -b feature/make-it-epic`
3. Commit your changes: `git commit -m "feat: make it more epic"`
4. Push: `git push origin feature/make-it-epic`
5. Open a PR and let Copilot review it

---

## 📜 License

This project is open-source. Use it, remix it, demo it, impress your colleagues. Just don't use it for evil — *"We don't negotiate with bugs."* 🕷️

---

<p align="center">
  Built with <span style="color:#f85149;">♥</span> using <strong>Streamlit</strong> &amp; <strong>Bootstrap 5</strong> — GitHub Copilot Demo © 2026
</p>
