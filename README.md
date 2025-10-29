### ERPNext AI

AI assistant and reporting for ERPNext admins. The app adds a role-aware AI Command Center that summarises
ERPNext activity and can generate OpenAI powered executive briefs.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app erpnext_ai
```

### Configuration

1. Assign the new **AI Manager** role to users who should access AI reports (System Managers retain full access).
2. Define your OpenAI credentials securely. Recommended approach: add `OPENAI_API_KEY=sk-...` to the bench-level `.env`
   (or `common_site_config.json`). The app will automatically pick this up; the field in **AI Settings** exists only as a
   fallback for air-gapped setups.
3. Review **AI Settings** (`Desk → Build → Chatting with AI → AI Settings`) to configure provider, model, timeout and prompt.
   - Model selectors include `gpt-5`, `gpt-5-mini`, `gpt-4o`, `gpt-4o-mini`. Adjust the prompt template if you want to customise the summary style.
4. Make sure `bench start` (or the production services) are running; scheduler will then create a daily “AI Admin Summary”.

### Usage

- Navigate to **Desk → Build → Chatting with AI** to trigger summaries or open the chat workspace.
- Use **AI Chat** for interactive GPT‑5 Mini conversations grounded in ERPNext context. Messages are stored in
  `AI Conversation` records with optional ERP snapshots for auditability.
- The primary action on the AI Command Center page still triggers `generate_admin_summary`, which persists the report
  and renders the Markdown response inline.

### Telegram Sales Bot

This app ships with an optional Telegram bot (`erpnext_ai.telegram.bot`) that bridges ERPNext sales operations into group
chats. The bot supports the admin → sales master manager → sales manager workflow described in the project brief.

1. Define the required environment variables (bench-level `.env` or process environment):
   - `TELEGRAM_BOT_TOKEN` – BotFather token.
   - `TELEGRAM_ADMIN_IDS` – Comma separated Telegram user IDs allowed to register master managers.
   - `FRAPPE_BASE_URL` – Base URL of the ERPNext site (e.g., `https://erp.example.com`).
   - Optional hardening: `BOT_ENCRYPTION_KEY` (32‑byte key in urlsafe base64), `TELEGRAM_BOT_DB_PATH`, `TELEGRAM_REPORT_*` overrides.
2. Install the new dependencies (inside the bench environment): `pip install -e apps/erpnext_ai`.
3. Run the bot service:

```bash
# From your bench folder
bench --site your-site-name execute erpnext_ai.erpnext_ai.telegram.bot.main
# or directly via python (virtualenv must include frappe site packages):
python -m erpnext_ai.telegram.bot
```

The bot must be added to target groups as an administrator. Workflow recap:

- Admin (`TELEGRAM_ADMIN_IDS`) → `/add_master_manager <telegram_id>` in private chat.
- Sales master manager joins target groups, runs `/users`, then picks the future sales manager from the inline list.
- Sales manager receives a DM prompting `/set_api <api_key> <api_secret>`. Credentials are verified against ERPNext and stored encrypted.
- Group users can now invoke `/report` for recent ERPNext sales data and `/order` to submit a structured request. Orders are saved as ERPNext leads and logged locally for auditing.

A lightweight SQLite database (path configurable via `TELEGRAM_BOT_DB_PATH`) tracks assignments and order history.

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/erpnext_ai
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
