# Orbdent People2025

A SaaS for Orbdent, built with FastAPI, React, TailAdmin (free), and PostgreSQL. Deployed on Fly.io at `people2025.orbdent.com`.

## Build Requirements
- **Backend**:
  - Python 3.11
  - Dependencies: See `backend/requirements.txt`
  - Tools: Docker, Gunicorn
- **Frontend**:
  - Node.js 18
  - Dependencies: See `frontend/package.json`
  - Tools: Vite
- **Deployment**:
  - Fly.io CLI (`flyctl`)
  - Docker
- **Database**:
  - PostgreSQL (Fly.io-hosted)
  - Credentials: `orbdeqio_people`, `orbdeqio_user_people`, `*4A6jds.egXF`

## Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Fly.io CLI (`flyctl`)
- Git
- Beekeeper Studio

### Local Development
1. **Clone**:
   ```bash
   git clone https://github.com/SmileworksAS/people2025.git
   cd people2025
