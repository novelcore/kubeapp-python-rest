# CI/CD Workflow Documentation

## Overview

This document describes the CI/CD workflow implemented in this repository, which follows a GitOps approach for software development and deployment. The workflow is designed to support continuous integration, semantic versioning, and progressive delivery through different environments.

## Branch Structure

### Main Branches

- **main**: Production-ready code that has passed all tests and approvals
- **dev**: Integration branch for ongoing development
- **rc/vX.Y.Z**: Release candidate branches for preparing releases

### Feature Branches

All development work is done in feature branches that follow specific naming conventions:

- **feature/\***: New features or enhancements (triggers minor version bump)
- **bugfix/\*** or **bug/\***: Non-critical bug fixes (triggers patch version bump)
- **breaking/\***: Changes that break backward compatibility (triggers major version bump)
- **maintenance/\***: Maintenance tasks (triggers patch version bump)
- **chore/\***: Housekeeping tasks, dependency updates (no version bump)
- **hotfix/\***: Critical fixes for production issues (triggers patch version bump)

## Workflow Stages

### 1. Development in Feature Branches

1. Developer creates a branch from `dev` using the appropriate naming convention:
   ```bash
   git checkout -b feature/new-capability
   ```

2. When the branch is pushed, the CI pipeline:
   - Builds the code
   - Creates a Docker image tagged with the branch type, timestamp, and commit hash
   - Pushes the image to the container registry

### 2. Pull Request to Dev

1. Developer opens a PR to merge the feature branch into `dev`
2. The PR workflow:
   - Validates branch naming
   - Adds a comment with branch type and version impact
   - When merged, calculates the appropriate version bump

### 3. Merge to Dev

When a PR is merged to `dev`, the following occurs:

1. A new semantic version is calculated based on the branch type
2. A new Docker image is built with the tag `dev-vX.Y.Z-{timestamp}-{hash}`
3. A Git tag is created with the format `dev-vX.Y.Z`
4. The GitOps repository is notified to deploy to the dev environment

### 4. Release Candidate Creation

1. When ready to prepare a release:
   ```bash
   # Triggered via GitHub Actions UI
   # Input: Version (e.g., 1.2.0) and RC number (default: 1)
   ```

2. This creates:
   - A `rc/vX.Y.Z` branch from `dev`
   - A Git tag `vX.Y.Z-rc1`
   - A Docker image tagged as `vX.Y.Z-rc1-{timestamp}-{hash}`
   - A PR from the RC branch to `main`
   - A notification to the GitOps repository to deploy to staging

### 5. Release Candidate Iterations

If issues are found in staging:

1. Fix is applied directly to the RC branch:
   ```bash
   git checkout rc/vX.Y.Z
   # Make fixes
   git commit -m "Fix issue in RC"
   git push
   ```

2. This triggers:
   - A new Docker image with an incremented RC number: `vX.Y.Z-rc2-{timestamp}-{hash}`
   - A new Git tag `vX.Y.Z-rc2`
   - A notification to update the staging environment

### 6. Production Release

When the RC is approved:

1. The PR from `rc/vX.Y.Z` to `main` is merged
2. This triggers:
   - A final production Docker image tagged as `vX.Y.Z` and `latest`
   - A Git tag `vX.Y.Z`
   - A notification to the GitOps repository to deploy to production
   - A GitHub Release is created
   - The `dev` branch is synchronized with `main`

### 7. Hotfixes

For critical production issues:

1. Developer creates a branch from `main`:
   ```bash
   git checkout -b hotfix/critical-issue
   ```

2. When ready, a PR is created to merge to `main` (bypassing `dev`)
3. When merged:
   - Patch version is incremented: `vX.Y.Z+1`
   - A Docker image is created with the tag `vX.Y.Z+1-hotfix-{hash}`
   - A Git tag `vX.Y.Z+1` is created
   - A notification is sent to update production
   - A PR is automatically created to sync the hotfix back to `dev`

## Image Tagging Strategy

| Branch Type | Image Tag Format | Example |
|-------------|------------------|---------|
| Feature | `feature-{timestamp}-{hash}` | `feature-20230506123045-abc1234` |
| Development | `dev-vX.Y.Z-{timestamp}-{hash}` | `dev-v1.2.0-20230506123045-def5678` |
| Release Candidate | `vX.Y.Z-rcN-{timestamp}-{hash}` | `v1.2.0-rc1-20230506123045-ghi9012` |
| Hotfix | `vX.Y.Z-hotfix-{hash}` | `v1.2.1-hotfix-jkl3456` |
| Release | `vX.Y.Z` | `v1.2.0` |

## Version Bump Strategy

| Branch Prefix | Version Bump | Example |
|---------------|--------------|---------|
| `feature/*` | Minor | `1.0.0` → `1.1.0` |
| `breaking/*` | Major | `1.0.0` → `2.0.0` |
| `bug/*` or `bugfix/*` | Patch | `1.0.0` → `1.0.1` |
| `maintenance/*` | Patch | `1.0.0` → `1.0.1` |
| `chore/*` | None | No version change |
| `hotfix/*` | Patch | `1.0.0` → `1.0.1` |

## GitOps Integration

The CI pipelines integrate with the GitOps repository (`kubeproject-template`) through repository dispatch events:

1. **Dev Environment Update**:
   - Triggered when a PR is merged to `dev`
   - Updates the dev environment configuration

2. **Staging Environment Update**:
   - Triggered when an RC is created or updated
   - Updates the staging environment configuration

3. **Production Environment Update**:
   - Triggered when an RC is merged to `main`
   - Updates the production environment configuration

4. **Production Hotfix Update**:
   - Triggered when a hotfix is merged to `main`
   - Updates the production environment with high priority

## Common Development Workflows

### Creating a New Feature

```bash
# Create feature branch from dev
git checkout dev
git pull
git checkout -b feature/amazing-new-feature

# Do work and commit changes
git add .
git commit -m "Implement amazing new feature"
git push -u origin feature/amazing-new-feature

# Open PR to dev branch through GitHub UI
# When merged, this will:
# 1. Trigger a minor version bump
# 2. Build dev image
# 3. Update dev environment
```

### Fixing a Bug

```bash
# Create bugfix branch from dev
git checkout dev
git pull
git checkout -b bugfix/fix-validation-issue

# Fix the bug and commit
git add .
git commit -m "Fix validation issue"
git push -u origin bugfix/fix-validation-issue

# Open PR to dev branch through GitHub UI
# When merged, this will:
# 1. Trigger a patch version bump
# 2. Build dev image
# 3. Update dev environment
```

### Creating a Release Candidate

```
# Through GitHub Actions UI:
# 1. Select the "Release Candidate Workflow"
# 2. Input the version (e.g., 1.2.0)
# 3. Run workflow

# This will:
# 1. Create the rc/v1.2.0 branch
# 2. Tag it as v1.2.0-rc1
# 3. Build and deploy to staging
# 4. Create PR to main
```

### Creating a Hotfix

```bash
# Create hotfix branch from main
git checkout main
git pull
git checkout -b hotfix/critical-fix

# Fix the issue and commit
git add .
git commit -m "Fix critical production issue"
git push -u origin hotfix/critical-fix

# Open PR to main branch through GitHub UI
# When merged, this will:
# 1. Trigger a patch version bump
# 2. Build production image
# 3. Update production environment
# 4. Create PR to sync changes back to dev
```

## Required Secrets and Variables

### Repository Secrets

- `REGISTRY_URL_V2`: URL of the container registry
- `CI_BOT_REGISTRY_NAME_V2`: Username for container registry
- `CI_BOT_REGISTRY_PWD_V2`: Password for container registry
- `GH_APP_ID`: GitHub App ID for token generation
- `GH_APP_PRIVATE_KEY`: GitHub App private key for token generation

### Repository Variables

- `PROJECT_NAME`: Name of the GitOps project
- `BASE_PROJECT_DOMAIN`: Base domain for deployments
- `RUNNER`: JSON array defining the GitHub Actions runner to use

## Conclusion

This CI/CD workflow provides a structured approach to development, versioning, and deployment through a GitOps model. By following the branch naming conventions and understanding the automated processes, teams can efficiently develop and release software with confidence.
