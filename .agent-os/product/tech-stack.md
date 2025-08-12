# Technical Stack

> Last Updated: 2025-08-12
> Version: 1.0.0

## Application Framework

- **Framework:** Python CLI Application
- **Version:** 3.6+

## Database

- **Primary Database:** JSON Configuration Files (File System)

## JavaScript

- **Framework:** Not applicable (CLI application)

## CSS Framework

- **Framework:** Not applicable (CLI application)

## UI Component Library

- **Library:** Command Line Interface (CLI)

## Fonts Provider

- **Provider:** System Terminal Fonts

## Icon Library

- **Library:** CLI Text Characters

## AI Integration

- **Primary AI Platform:** Claude Code CLI by Anthropic
- **Version:** Latest available
- **Integration:** Direct CLI commands for content analysis and generation

## Configuration Management

- **Format:** JSON configuration files
- **Location:** config/agent_collections.json
- **Agent Prompts:** Text files in prompts/ directory structure

## Output Format

- **Primary Format:** Markdown (.md) for analysis outputs
- **Content Format:** Text files (.txt) with semantic versioning
- **Metadata:** JSON session summaries

## Version Control

- **Repository Platform:** Git
- **Code Repository URL:** https://github.com/iamseb/claude-writing-assistant.git

## Application Hosting

- **Hosting:** Local development environment / User workstation
- **Deployment:** Direct execution via Python script

## Asset Hosting

- **Assets:** Local file system (prompts, configurations, examples)

## Deployment Solution

- **Solution:** Direct installation via setup.sh script
- **Distribution:** Git repository cloning
- **Dependencies:** Python 3.6+, curl (for Claude Code installation)

## Development Tools

- **Primary Language:** Python 3.6+
- **Shell Integration:** Bash scripts for setup and automation
- **Text Processing:** Native Python file I/O
- **CLI Framework:** Native Python argparse

## File Structure

- **Input Processing:** Plain text files
- **Configuration:** JSON for agent collections
- **Prompts:** Text files organized by collection
- **Output:** Structured directories with timestamped sessions