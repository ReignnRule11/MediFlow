# MediFlow deployment targets

MediFlow is being kept as a multi-target project. The GitHub Pages site is an additional static product demo, not a replacement for the application source.

## 1. GitHub Pages demo

- Source: `site/`
- Entry point: `site/index.html`
- Workflow: `.github/workflows/pages.yml`
- Expected URL: https://reignnrule11.github.io/MediFlow/
- Hosting: GitHub Pages (static HTML/CSS/JavaScript)
- Data: fictional, hard-coded demonstration data only
- API: not connected

After merging the Pages changes into `main`, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**. The workflow then publishes the `site/` directory. A green workflow run and a successful browser smoke test are required before calling the site live.

## 2. Full application deployment (separate platform)

Keep the application architecture and deploy its services independently:

| Component | Intended deployment |
| --- | --- |
| Frontend | Next.js hosting platform (for example, Vercel) |
| Backend | Python/FastAPI container hosting |
| Database | Managed PostgreSQL |
| Cache / background jobs | Managed Redis and worker service, if required |
| Documents | Private object storage with access controls |

The repository archive currently contains many flattened implementation fragments rather than the complete directory layout described in its README. Before deploying the full application, reconstruct and validate the actual frontend/backend package structure, dependencies, migrations, tests, and environment configuration. Do not point the static demo at localhost or imply it is using a live API.

## 3. Production safeguards

- Never commit real patient records, credentials, API keys, signing secrets, or production environment files.
- Use synthetic data only in the public Pages demo.
- Configure the full application API URL through platform environment variables.
- Restrict CORS to the actual application origins.
- Use managed database credentials and rotate any exposed secrets.
- Validate authentication, authorization, upload limits, audit logging, backups, and clinical safety boundaries before production use.
- GitHub Pages cannot host FastAPI, PostgreSQL, Redis, private uploads, or server-side secrets.

## 4. Deployment separation

The Pages workflow only packages `site/`. It does not modify, build, or delete the original application source, API, database schema, or documentation. Other deployment workflows can be added alongside it for the full application.
