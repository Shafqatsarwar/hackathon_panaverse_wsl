---
name: github_skill
description: Skill for GitHub interactions (listing repos, checking commits)
---

# GitHub Skill

This skill handles interaction with GitHub API.

## Capabilities

- List repositories
- Get recent commits

## Usage

```python
from skills.github_skill.skill import GitHubSkill

skill = GitHubSkill(token="...")
repos = skill.list_repos()
```

## Configuration

Requires `GITHUB_TOKEN` in `.env`.
