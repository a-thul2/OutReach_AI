# 🚀 OutReach_AI

> **AI-curated cold outreach that sends only the best message.**

OutReach_AI is an **agentic AI workflow** that generates multiple cold sales email drafts using distinct AI sales personas, evaluates them automatically, and **sends only the single best email**—no spam, no guesswork.

Unlike traditional AI email generators, OutreachAI enforces **quality through consensus**.

---

## ✨ Key Features

- 🤖 **Multi-Agent Drafting**  
  Three specialized AI sales agents generate cold emails with different styles:
  - Professional
  - Engaging / Humorous
  - Concise / Executive

- 🧠 **AI-Driven Evaluation**  
  A Sales Manager agent reviews all drafts and selects the most effective one.

- 📤 **Single-Send Guarantee**  
  Exactly **one email** is sent—never more, never less.

- 🔒 **Enterprise-Friendly Design**  
  Built with deterministic rules, and tool enforcement

- 🔌 **Pluggable LLM Backend**  
  Uses Gemini via OpenAI-compatible routing (easily extendable).

---

## 🛠️ Tech Stack

- Python 3.10+
- OpenAI Agents SDK
- Gemini (OpenAI-compatible API)
- SendGrid
- AsyncIO
- python-dotenv

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/outreachai.git
cd outreachai
````

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY = your_gemini_api_key
SENDGRID_API_KEY = your_sendgrid_api_key
FROM_EMAIL = your_sendgrid_verified_email
TO_EMAIL = recipient_email
```

---

### 4️⃣ Run the Workflow

```bash
python app.py
```

Example input:

```text
Send a cold sales email addressed to "Dear CEO"
```

---

## 🧠 How OutReach_AI Works

1. **Draft Generation**
   Each sales agent independently generates a cold email.

2. **Evaluation**
   The Sales Manager agent reviews all drafts and selects the strongest one.

3. **Execution**
   The selected email is sent using the `send_email` tool.

Strict enforcement ensures:

* Agents must be used for drafting
* The manager cannot write emails directly
* Only **one email** is ever sent

---

## 🧪 Example Use Cases

* B2B cold outreach
* Founder-led sales automation
* SDR assistance
* High-signal prospecting
* Compliance-aware AI sales tooling

---
