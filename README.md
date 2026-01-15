# Hidden Gems Newsletter 💎

Automatically discover trending new GitHub repositories with 50+ stars from the past week.

## Overview

This project uses the GitHub CLI to search for newly created repositories that are gaining traction quickly. It runs daily via GitHub Actions and maintains an updated list of "hidden gems" - repositories that might be the next big thing.

## How It Works

The `gems.sh` script:
- Searches for repositories created in the last 7 days
- Filters for repos with at least 50 stars
- Fetches the top 50 results sorted by star count
- Saves the results to `gems.json` with key metadata

Each repository entry includes:
- **createdAt**: When the repository was created
- **stars**: Current star count
- **name**: Full repository name (owner/repo)
- **url**: Repository URL
- **lang**: Primary programming language
- **desc**: Repository description

## Automation

A GitHub Actions workflow runs daily at 22:00 UTC to:
1. Execute `gems.sh` to fetch fresh data
2. Automatically commit and push changes to `gems.json`

You can also manually trigger the workflow from the Actions tab.

## Usage

### Prerequisites

- [GitHub CLI](https://cli.github.com/) installed and authenticated
- `jq` for JSON processing

### Running Locally

```bash
./gems.sh
```

This will update `gems.json` with the latest trending repositories.

### Configuration

You can modify the search parameters in `gems.sh`:

```bash
DAYS_BACK=7          # how many days of history
STAR_MIN=50          # minimum stars
LIMIT=50             # how many repos to fetch
```

## Example Output

```json
[
  {
    "createdAt": "2026-01-11T05:38:15Z",
    "stars": 4755,
    "name": "vercel-labs/agent-browser",
    "url": "https://github.com/vercel-labs/agent-browser",
    "lang": "TypeScript",
    "desc": "Browser automation CLI for AI agents"
  }
]
```

## Use Cases

- Stay updated on trending new projects
- Discover emerging tools and libraries
- Track the GitHub open source ecosystem
- Build a newsletter or digest of new repositories
- Research trending technologies and frameworks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
