<!--
==============================================================================
                               AI GENERATION PROMPT
==============================================================================

PROMPT FOR AI TO GENERATE A COMPLETE README.md:

Review the entire repository structure to generate a comprehensive README.md file. This README MUST BE WRITTEN IN ENGLISH.

Key requirements to consider:
- Include a brief description of what this repository is for and its main purpose
- Explain how to install dependencies (include both basic and developer installations)
- Detail how to use the repository (CLI commands, API usage, etc.)
- Provide project structure (exclude common files like __init__.py, focus on important directories and files)
- List development tools and workflows
- Include configuration management details
- Add deployment instructions if applicable
- Mention testing procedures
- List future improvements or known issues

Instructions for content generation:
1. Replace ALL placeholders marked with [PLACEHOLDER] with actual values
2. Remove sections that don't apply to this specific project
3. Add concrete examples and commands based on the actual project files
4. Focus on practical usage and clear instructions
5. Ensure all links and references point to actual files/directories
6. KEEP THE COMMENTS OF THE IA PROMPTS, TO BE USED IN THE FUTURE TO UPDATE THE CONTENT OF THE PROMPTS
7. Do not include any dependency that can be obtained from pyproject.toml
8. Look up in *.lock or pyproject.toml which project manager is being used, and use it to execute commands.
9. Execute the commands you write in the README.md to check that they are well written and test that they work. Use the project manager deduced in the step 8. and remove the virtual environment prior the commands testing.
10. Get the exact python version from .python-version
11. Avoid using statements like `export VARIABLE=variable` (they will be defined in the .env file)
12. If there is no previous repository provided, ask what was the previous repository before starting the whole documentation generation process.
13. If the project uses pre-commit, avoid mentioning individual linting/formatting tools (ruff, mypy, pylint, black, isort, etc.) since pre-commit should already handle these requirements. Focus on pre-commit setup and usage instead.
14. Avoid listing specific environment variables in the README. Instead, simply reference the .env.example file and instruct users to copy it and rename it as .env (e.g., "cp .env.example .env"). This prevents documentation duplication and keeps environment variable details centralized.

Use the template structure below as a foundation, but adapt it to match the specific project type and requirements.

==============================================================================
-->

![Logo](https://storage.googleapis.com/basic-resources/bloom%20logo%20color.svg)

# [PROJECT_NAME]

<!-- AI PROMPT: Write a 2-3 sentence summary of what this project does. Focus on the main functionality and value proposition. -->
[Brief project description - what does this project do and why is it useful?]

<!-- AI PROMPT: If this project replaces or is based on a previous version, mention it here. Otherwise, remove this section. -->
The previous version of this repository was [previous-repo-name](https://github.com/[ORG]/[previous-repo-name])

## Project Description

<!-- AI PROMPT: Provide a detailed description of the project including:
- Main functionality and workflow
- Key features and capabilities
- Target use cases or problems it solves
Use bullet points for the main processes if applicable -->

This project implements [main functionality description]:

- **[Feature 1]**: [Description]
- **[Feature 2]**: [Description]
- **[Feature 3]**: [Description]

### [Specific Feature Section - e.g., "Supported Data Types", "Available Models", etc.]

<!-- AI PROMPT: If your project has specific categories, types, or models it supports, list them here with descriptions. Otherwise, remove this section. -->

The [system/pipeline/application] supports the following [categories/types/models]:

- **[TYPE-01]**: [Description]
- **[TYPE-02]**: [Description]
- **[TYPE-03]**: [Description]

## Installation

### Prerequisites

<!-- AI PROMPT: List all prerequisites needed to run this project. Include:
- Python version (if Python project)
- Package managers (poetry, uv, pip, etc.)
- External services or APIs
- Cloud platform accounts (if applicable)
- Database requirements -->

- Python [X.X.X]
- [Package manager](fttps://package-manager-link.com) (recommended)
- Access to [External service/API]
- [Cloud platform] account (for cloud deployment)

### Basic Installation

```bash
# Create virtual environment
[command to create venv using the [Package manager]]
# [EXAMPLE: uv venv]

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies using [Package manager] (recommended)
[recommended installation command]
# [EXAMPLE: uv sync --no-dev]

# Alternative: Install with pip
[alternative installation command]
# [EXAMPLE: pip install .]
```

### Development Installation

```bash
# Install with development dependencies
[dev installation command]
# [EXAMPLE: uv sync --dev]

# Alternative: Install with pip
[alternative dev installation command]
# [EXAMPLE: pip install -e ".[dev]"]

# Copy environment variables template
cp .env.example .env
# (Fill in the missing values)
```

#### [Quality Tools - e.g., "Pre-commit Hooks", "Linting", "Testing"]

<!-- AI PROMPT: If the project uses code quality tools like pre-commit, linting, or testing frameworks, describe them here. Otherwise, remove this section. -->

The project uses [quality tools] for automated code quality:

```bash
# Install quality tools
[installation command]
# [EXAMPLE: pre-commit install]

# Run quality checks
[run command]
# [EXAMPLE: pre-commit run --all-files]

# Update tool versions
[update command]
# [EXAMPLE: pre-commit autoupdate]
```

### Logging and Debugging

<!-- AI PROMPT: If the project has logging or debugging features, describe how to enable them. Otherwise, remove this section. -->

Enable comprehensive logging for troubleshooting:

```bash
# Enable debug logging
[debug command with example]
# [EXAMPLE: python -m src --max-level-logging "DEBUG"]
```

## Local Development and Testing

<!-- AI PROMPT: Provide instructions for local development and testing. Include:
- How to run tests
- How to run the application locally
- How to test specific components
Adjust based on the project type (web app, CLI tool, library, etc.) -->

### [Testing Section - e.g., "Running Tests", "Testing Locally"]

Please refer to [path/to/testing/docs](./path/to/testing/docs) for detailed testing instructions.

```bash
# Run all tests
[test command]

# Run specific test category
[specific test command]
```

## Usage

### Command Line Interface

<!-- AI PROMPT: If your project has a CLI, describe how to use it. If it's a library or web service, adjust this section accordingly. -->

The [application/pipeline] provides a [CLI/API/web interface]:

```bash
# Basic usage
[basic command example]
```

### [CLI/API/Configuration] Parameters

<!-- AI PROMPT: List all available parameters, grouped by required vs optional. Include data types and examples. -->

**Required Parameters:**

- `--[param-name]`: [Description] (format: [format])

**Optional Parameters:**

- `--[param-name]`: [Description] (default: [default-value])
- `--[param-name]`: [Description] (format: [format])

## Project Structure

<!-- AI PROMPT: Generate the project structure tree based on the actual project files. Focus on the main directories and important files. Exclude common files like __init__.py, __pycache__, .git, etc. -->

```
.
├── src/                          # Main source code
│   ├── __main__.py              # [Entry point description]
│   ├── [module1]/
│   │   └── [file1].py           # [File description]
│   ├── [module2]/               # [Module description]
│   │   ├── [file2].py           # [File description]
│   │   └── [file3].py           # [File description]
│   └── utils/                   # Utility modules
│       ├── [util1].py           # [Utility description]
│       └── [util2].py           # [Utility description]
├── [additional_folder]/         # [Folder description]
│   └── [subfolder]/             # [Subfolder description]
│       ├── [file].py            # [File description]
│       └── requirements.txt     # [Dependencies description]
├── Dockerfile                   # [Container description]
├── pyproject.toml              # Project dependencies and configuration
└── [lock_file]                 # Dependency lock file
```

## Configuration Management

<!-- AI PROMPT: Describe how configuration is managed in the project. Include:
- Configuration files locations (usually located in ./src/config/params.py)
- Environment variables needed
- How to modify settings
- Examples of common configurations -->

The configuration is managed through [configuration method]:

- **Configuration files**: Located in [`path/to/config`](./path/to/config)
- **Environment variables**: [List key environment variables]
- **[Other configuration methods]**: [Description]

## Deployment

<!-- AI PROMPT: If the project can be deployed (cloud, containers, etc.), provide deployment references. Include links to CI/CD pipeline files, workflow definitions, and deployment documentation. Otherwise, remove this section. -->

### Continuous Integration and Deployment

<!-- AI PROMPT: Review the actual CI/CD configuration files in the project (.github/workflows/, workflows/, Dockerfile, etc.) and describe:
- Which files contain the deployment configuration
- What platforms or services are used (GitHub Actions, Google Cloud Workflows, Docker, etc.)
- Links to the actual configuration files
- Brief description of what each file does
If no CI/CD is configured, remove this subsection. -->

The project includes automated deployment pipelines configured in the following files:

- **CI/CD Pipeline**: See [`.github/workflows/cicd.yaml`](./.github/workflows/cicd.yaml) for GitHub Actions configuration
- **Google Cloud Workflows**: See [`workflows/workflows.yaml`](./workflows/workflows.yaml) for cloud workflow definitions
- **Docker Configuration**: See [`Dockerfile`](./Dockerfile) for containerization setup

### Deployment Process

<!-- AI PROMPT: Describe the actual deployment triggers and process based on the CI/CD configuration files. Include:
- What events trigger deployments (branch merges, tags, manual triggers)
- Which branches are used for different environments (staging, prod, etc.)
- What happens during deployment (build, test, deploy steps)
- Any manual steps required
- Environment-specific configurations
If deployment is manual only, adjust this section accordingly. -->

The deployment automatically triggers on:

- Pull requests merged to `staging` or `prod` branches
- Changes to source code, workflows, or Docker configuration
- Manual workflow dispatch

## API Documentation

<!-- AI PROMPT: If the project exposes an API or uses external APIs, provide documentation or links to it. Otherwise, remove this section. -->

[API documentation location or brief description of endpoints]

## Future Steps

<!-- AI PROMPT: List known issues, desired features, or roadmap items. Use checkboxes for better visibility. -->

Known issues and desired features for the future:

- [ ] [Feature or improvement description]
- [ ] [Bug fix or enhancement description]
- [ ] [Future development goal]

<!--
==============================================================================
                           TEMPLATE USAGE INSTRUCTIONS
==============================================================================

INSTRUCTIONS FOR USING THIS TEMPLATE:

1. SEARCH AND REPLACE: Use find/replace to update all placeholders:
   - [PROJECT_NAME] → Actual project name
   - [ORG] → Organization/username
   - [X.X.X] → Version numbers
   - [commands] → Actual commands
   - [descriptions] → Actual descriptions

2. CONTENT GENERATION: For each section marked with "AI PROMPT:", use the provided
   instructions to generate specific content based on the actual project.

3. SECTION REMOVAL: Remove sections that don't apply to your specific project
   (e.g., API Documentation for CLI-only tools).

4. CUSTOMIZATION: Adjust the structure and sections based on your project type:
   - Web applications: Add deployment, API sections
   - Libraries: Focus on installation, usage examples
   - CLI tools: Emphasize command-line usage
   - Data pipelines: Detail the ETL/processing flow

5. EXAMPLES: Add concrete examples and code snippets relevant to your project.

6. MAINTENANCE: Keep the README updated as the project evolves.

7. VALIDATION: Ensure all links point to actual files and all commands work.

==============================================================================
-->
