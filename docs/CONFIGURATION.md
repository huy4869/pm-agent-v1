# Configuration

## 1. Environment strategy

Scripts and application code should load the repository `.env` through `python-dotenv`, allowing test/setup utilities to reuse the same Jira/model/delivery credentials.

Never commit the real `.env`.

## 2. Project data source

Select one source per run. Jira remains the default for backward compatibility:

```dotenv
PM_SOURCE=jira
```

Use `PM_SOURCE=redmine` to collect from Redmine instead. Redmine issue IDs are
normalized as `RM-123` inside snapshots and reports.

### Jira

Observed V6/test tooling uses these variables:

```dotenv
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=replace_me
JIRA_PROJECT_KEY=DEV
```

### Redmine

Enable the REST API in Redmine, copy the API key from **My account**, and use
the numeric project ID (not the project identifier):

```dotenv
PM_SOURCE=redmine
REDMINE_BASE_URL=https://redmine.example.com
REDMINE_API_KEY=replace_me
REDMINE_PROJECT_ID=1
```

The collector reads open and closed issues, follows Redmine pagination, imports
parent links and issue relations, and uses journals to reconstruct status history.

Test-sprint utilities may also use:

```dotenv
JIRA_TEST_SPRINT_NAME=PM Agent Test Sprint 1
JIRA_TEST_SPRINT_ISSUES=35
JIRA_TEST_SPRINT_DAYS=14
```

## 3. AI provider

Keep provider configuration behind an adapter. The exact variable names are implementation-specific and should match the source tree. A typical deployment needs provider/model selection, API key, timeout/retry controls and optional temperature/max-output settings.

Do not put model-provider secrets into reports or logs.

## 4. Telegram / Teams

Delivery should be adapter-based. Telegram requires a bot credential and target chat/channel identifier. Microsoft Teams should use the chosen Graph/bot/workflow integration and its corresponding tenant/app/channel identifiers.

Keep delivery disabled or pointed at a test destination during mutation tests.

## 5. Timezone

Daily reports should use a configured project timezone. For the current DEV test setup the observed report timestamps use UTC+07:00. Avoid mixing UTC timestamps with local due-date interpretation without explicit conversion.

## 6. Suggested `.env.example`

```dotenv
# Jira
PM_SOURCE=jira
JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=
JIRA_PROJECT_KEY=DEV

# Redmine (used instead of Jira when PM_SOURCE=redmine)
REDMINE_BASE_URL=
REDMINE_API_KEY=
REDMINE_PROJECT_ID=

# Test sprint
JIRA_TEST_SPRINT_NAME=PM Agent Test Sprint 1
JIRA_TEST_SPRINT_ISSUES=35
JIRA_TEST_SPRINT_DAYS=14

# AI (use names implemented by your provider adapter)
AI_PROVIDER=
AI_MODEL=
AI_API_KEY=

# Delivery (use only adapters enabled in source)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Runtime
PROJECT_TIMEZONE=Asia/Ho_Chi_Minh
```

Treat unspecified AI/delivery names above as documentation placeholders until they are matched to the concrete source configuration.

## Resource Allocation

The interactive Telegram bot reads optional team skill profiles from:

```dotenv
RESOURCE_PROFILE_FILE=data/resources.json
```

Start from `data/resources.example.json`, keep the real team profile local, and run the bot with `python main.py bot`.
