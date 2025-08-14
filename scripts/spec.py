#!/usr/bin/env python3
"""
Spec Management System
A CLI tool for creating, tracking, and managing feature specifications using Agent OS conventions.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import re
import tempfile
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, TemplateSyntaxError


class SpecManager:
    """Main class for managing specification lifecycle and operations."""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        self.specs_dir = self.project_root / ".agent-os" / "specs"
        self.templates_dir = self.project_root / "templates" / "specs"
        
        # Configuration files
        self.status_db_file = self.config_dir / "spec_status.json"
        self.templates_config_file = self.config_dir / "spec_templates.json"
        
        # Ensure required directories exist
        self._ensure_directories()
        
        # Load configurations
        self.status_db = self._load_status_db()
        self.templates_config = self._load_templates_config()
        
        # Initialize status tracker and template engine
        self.status_tracker = StatusTracker(self)
        self.template_engine = TemplateEngine(self)
    
    def _ensure_directories(self):
        """Ensure all required directories exist with proper permissions."""
        try:
            # Create config directory (similar to write.py pattern)
            self.config_dir.mkdir(exist_ok=True)
            
            # Create Agent OS specs directory
            self.specs_dir.mkdir(parents=True, exist_ok=True)
            
            # Create templates directory
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            
        except OSError as e:
            raise FileNotFoundError(f"Failed to create required directories: {e}")
    
    def _load_status_db(self):
        """Load the spec status database from JSON file."""
        if not self.status_db_file.exists():
            # Create empty status database
            initial_db = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "specs": {}
            }
            self._save_status_db(initial_db)
            return initial_db
        
        try:
            with open(self.status_db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in spec status database {self.status_db_file}: {e}")
        except OSError as e:
            raise FileNotFoundError(f"Cannot read spec status database {self.status_db_file}: {e}")
    
    def _save_status_db(self, status_db=None):
        """Save the spec status database to JSON file with atomic write."""
        if status_db is None:
            status_db = self.status_db
        
        status_db["last_updated"] = datetime.now().isoformat()
        
        try:
            # Atomic write: write to temp file first, then rename
            temp_file = self.status_db_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(status_db, f, indent=2, ensure_ascii=False)
            temp_file.replace(self.status_db_file)
        except OSError as e:
            raise RuntimeError(f"Failed to save spec status database: {e}")
    
    def _load_templates_config(self):
        """Load the templates configuration from JSON file."""
        if not self.templates_config_file.exists():
            # Create default templates configuration
            default_config = {
                "version": "1.0.0",
                "templates": {
                    "collection": {
                        "name": "Agent Collection",
                        "description": "Specification for creating new agent collections",
                        "template_file": "collection.md.j2",
                        "required_fields": ["name", "description", "agents", "use_cases"]
                    },
                    "agent": {
                        "name": "Individual Agent",
                        "description": "Specification for creating individual agents",
                        "template_file": "agent.md.j2",
                        "required_fields": ["name", "role", "expertise", "analysis_focus"]
                    },
                    "integration": {
                        "name": "External Integration",
                        "description": "Specification for external system integrations",
                        "template_file": "integration.md.j2",
                        "required_fields": ["name", "system_type", "integration_method", "security_requirements"]
                    },
                    "workflow": {
                        "name": "Workflow Enhancement",
                        "description": "Specification for process improvements and workflow changes",
                        "template_file": "workflow.md.j2",
                        "required_fields": ["name", "current_workflow", "proposed_workflow", "impact_analysis"]
                    }
                }
            }
            self._save_templates_config(default_config)
            return default_config
        
        try:
            with open(self.templates_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in templates configuration {self.templates_config_file}: {e}")
        except OSError as e:
            raise FileNotFoundError(f"Cannot read templates configuration {self.templates_config_file}: {e}")
    
    def _save_templates_config(self, config):
        """Save the templates configuration to JSON file."""
        try:
            with open(self.templates_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise RuntimeError(f"Failed to save templates configuration: {e}")
    
    def get_spec_directory_name(self, spec_name):
        """Generate Agent OS-compliant directory name for a spec."""
        # Format: YYYY-MM-DD-spec-name
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        # Clean the spec name to be filesystem-safe
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '-', spec_name.lower())
        clean_name = re.sub(r'-+', '-', clean_name)  # Replace multiple dashes with single
        clean_name = clean_name.strip('-')  # Remove leading/trailing dashes
        
        return f"{date_prefix}-{clean_name}"
    
    def list_available_templates(self):
        """List all available spec templates."""
        templates = self.templates_config.get("templates", {})
        for template_key, template_info in templates.items():
            print(f"{template_key}: {template_info['name']} - {template_info['description']}")
    
    def validate_spec_name(self, spec_name):
        """Validate that a spec name follows conventions."""
        if not spec_name:
            raise ValueError("Spec name cannot be empty")
        
        if len(spec_name) < 3:
            raise ValueError("Spec name must be at least 3 characters long")
        
        if len(spec_name) > 50:
            raise ValueError("Spec name must be no more than 50 characters long")
        
        # Check for valid characters (allow letters, numbers, spaces, hyphens, underscores)
        if not re.match(r'^[a-zA-Z0-9\s_-]+$', spec_name):
            raise ValueError("Spec name can only contain letters, numbers, spaces, hyphens, and underscores")
        
        return True
    
    def spec_exists(self, spec_dir_name):
        """Check if a spec directory already exists."""
        spec_path = self.specs_dir / spec_dir_name
        return spec_path.exists()
    
    def get_spec_status(self, spec_dir_name):
        """Get the current status of a spec."""
        return self.status_db.get("specs", {}).get(spec_dir_name, {}).get("status", "unknown")
    
    def list_specs(self, status_filter=None, spec_type_filter=None, format_output="table"):
        """List all specs with optional filtering."""
        specs = self.status_db.get("specs", {})
        
        # Apply filters
        filtered_specs = {}
        for spec_name, spec_data in specs.items():
            if status_filter and spec_data.get("status") != status_filter:
                continue
            if spec_type_filter and spec_data.get("type") != spec_type_filter:
                continue
            filtered_specs[spec_name] = spec_data
        
        if not filtered_specs:
            print("No specs found matching the criteria.")
            return
        
        if format_output == "json":
            print(json.dumps(filtered_specs, indent=2))
        elif format_output == "summary":
            for spec_name, spec_data in filtered_specs.items():
                status = spec_data.get("status", "unknown")
                spec_type = spec_data.get("type", "unknown")
                created = spec_data.get("created", "unknown")
                print(f"{spec_name}: {status} ({spec_type}) - created {created}")
        else:  # table format
            print(f"{'Spec Name':<40} {'Status':<15} {'Type':<15} {'Created':<12}")
            print("-" * 82)
            for spec_name, spec_data in filtered_specs.items():
                status = spec_data.get("status", "unknown")
                spec_type = spec_data.get("type", "unknown")
                created = spec_data.get("created", "unknown")[:10] if spec_data.get("created") else "unknown"
                print(f"{spec_name:<40} {status:<15} {spec_type:<15} {created:<12}")


class StatusTracker:
    """Class for managing spec status database operations with validation."""
    
    # Valid status transitions
    VALID_STATUSES = ["draft", "approved", "in-progress", "complete", "on-hold", "cancelled"]
    
    # Valid status transitions (from_status -> [allowed_to_statuses])
    STATUS_TRANSITIONS = {
        "draft": ["approved", "cancelled"],
        "approved": ["in-progress", "on-hold", "cancelled"],
        "in-progress": ["complete", "on-hold", "cancelled"],
        "complete": [],  # Final state
        "on-hold": ["in-progress", "cancelled"],
        "cancelled": []  # Final state
    }
    
    def __init__(self, spec_manager):
        self.spec_manager = spec_manager
    
    def validate_status(self, status):
        """Validate that the status is a valid status value."""
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Valid statuses: {', '.join(self.VALID_STATUSES)}")
        return True
    
    def validate_status_transition(self, current_status, new_status):
        """Validate that a status transition is allowed."""
        self.validate_status(new_status)
        
        if current_status == "unknown":
            # First time setting status - allow any valid status
            return True
        
        if current_status not in self.STATUS_TRANSITIONS:
            raise ValueError(f"Unknown current status: {current_status}")
        
        allowed_transitions = self.STATUS_TRANSITIONS[current_status]
        if new_status not in allowed_transitions:
            raise ValueError(f"Invalid status transition from '{current_status}' to '{new_status}'. "
                           f"Allowed transitions: {', '.join(allowed_transitions) if allowed_transitions else 'None (final status)'}")
        return True
    
    def update_spec_status(self, spec_dir_name, new_status, developer=None, priority=None, metadata=None):
        """Update the status of a spec with validation and atomic write."""
        if not self.spec_manager.spec_exists(spec_dir_name):
            raise ValueError(f"Spec directory does not exist: {spec_dir_name}")
        
        current_status = self.spec_manager.get_spec_status(spec_dir_name)
        self.validate_status_transition(current_status, new_status)
        
        # Get current spec data or create new entry
        spec_data = self.spec_manager.status_db.get("specs", {}).get(spec_dir_name, {})
        
        # Update status and metadata
        spec_data.update({
            "status": new_status,
            "last_updated": datetime.now().isoformat(),
            "status_history": spec_data.get("status_history", [])
        })
        
        # Add status change to history
        status_change = {
            "from_status": current_status,
            "to_status": new_status,
            "timestamp": datetime.now().isoformat(),
            "changed_by": os.getenv("USER", "unknown")
        }
        spec_data["status_history"].append(status_change)
        
        # Update optional fields
        if developer is not None:
            spec_data["developer"] = developer
        if priority is not None:
            spec_data["priority"] = priority
        if metadata is not None:
            spec_data["metadata"] = {**spec_data.get("metadata", {}), **metadata}
        
        # Update the database
        if "specs" not in self.spec_manager.status_db:
            self.spec_manager.status_db["specs"] = {}
        
        self.spec_manager.status_db["specs"][spec_dir_name] = spec_data
        self.spec_manager._save_status_db()
        
        return spec_data
    
    def create_spec_entry(self, spec_dir_name, spec_type, spec_name, developer=None, priority="medium"):
        """Create a new spec entry in the status database."""
        if spec_dir_name in self.spec_manager.status_db.get("specs", {}):
            raise ValueError(f"Spec entry already exists: {spec_dir_name}")
        
        spec_data = {
            "name": spec_name,
            "type": spec_type,
            "status": "draft",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "developer": developer,
            "priority": priority,
            "status_history": [{
                "from_status": "none",
                "to_status": "draft",
                "timestamp": datetime.now().isoformat(),
                "changed_by": os.getenv("USER", "unknown")
            }],
            "metadata": {}
        }
        
        if "specs" not in self.spec_manager.status_db:
            self.spec_manager.status_db["specs"] = {}
        
        self.spec_manager.status_db["specs"][spec_dir_name] = spec_data
        self.spec_manager._save_status_db()
        
        return spec_data
    
    def get_spec_details(self, spec_dir_name):
        """Get detailed information about a spec."""
        return self.spec_manager.status_db.get("specs", {}).get(spec_dir_name, {})
    
    def get_specs_by_status(self, status):
        """Get all specs with a specific status."""
        self.validate_status(status)
        specs = {}
        for spec_name, spec_data in self.spec_manager.status_db.get("specs", {}).items():
            if spec_data.get("status") == status:
                specs[spec_name] = spec_data
        return specs
    
    def get_specs_by_developer(self, developer):
        """Get all specs assigned to a specific developer."""
        specs = {}
        for spec_name, spec_data in self.spec_manager.status_db.get("specs", {}).items():
            if spec_data.get("developer") == developer:
                specs[spec_name] = spec_data
        return specs


class TemplateEngine:
    """Class for managing Jinja2 templates for spec generation."""
    
    def __init__(self, spec_manager):
        self.spec_manager = spec_manager
        self.templates_dir = spec_manager.templates_dir
        
        # Initialize Jinja2 environment
        try:
            self.env = Environment(
                loader=FileSystemLoader(str(self.templates_dir)),
                trim_blocks=True,
                lstrip_blocks=True,
                keep_trailing_newline=True
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize template environment: {e}")
    
    def list_available_templates(self):
        """List all template files available in the templates directory."""
        if not self.templates_dir.exists():
            return []
        
        template_files = []
        for template_file in self.templates_dir.glob('*.j2'):
            template_files.append(template_file.name)
        return sorted(template_files)
    
    def template_exists(self, template_name):
        """Check if a template file exists."""
        template_path = self.templates_dir / template_name
        return template_path.exists()
    
    def validate_template(self, template_name):
        """Validate that a template has correct Jinja2 syntax."""
        try:
            template = self.env.get_template(template_name)
            # Try to parse the template to catch syntax errors
            template.new_context()
            return True
        except TemplateNotFound:
            raise FileNotFoundError(f"Template not found: {template_name}")
        except TemplateSyntaxError as e:
            raise ValueError(f"Template syntax error in {template_name}: {e}")
        except Exception as e:
            raise RuntimeError(f"Template validation error: {e}")
    
    def get_template_variables(self, template_name):
        """Extract variable names from a template."""
        try:
            template = self.env.get_template(template_name)
            # Get undeclared variables (variables that need to be provided)
            undeclared = template.new_context().environment.meta.find_undeclared_variables(template.new_context().environment.parse(template.source))
            return sorted(list(undeclared))
        except Exception as e:
            raise RuntimeError(f"Failed to extract template variables: {e}")
    
    def validate_template_variables(self, template_name, variables):
        """Validate that all required variables are provided for a template."""
        template_config = self.spec_manager.templates_config.get("templates", {})
        
        # Check if template is configured
        template_key = template_name.replace('.md.j2', '').replace('.j2', '')
        if template_key in template_config:
            required_fields = template_config[template_key].get("required_fields", [])
            missing_fields = []
            
            for field in required_fields:
                if field not in variables or not variables[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                raise ValueError(f"Missing required template variables: {', '.join(missing_fields)}")
        
        return True
    
    def render_template(self, template_name, variables, validate_variables=True):
        """Render a template with provided variables."""
        try:
            # Validate template exists and syntax is correct
            self.validate_template(template_name)
            
            # Validate variables if requested
            if validate_variables:
                self.validate_template_variables(template_name, variables)
            
            # Load and render template
            template = self.env.get_template(template_name)
            rendered_content = template.render(**variables)
            
            return rendered_content
            
        except Exception as e:
            raise RuntimeError(f"Failed to render template {template_name}: {e}")
    
    def create_sample_template(self, template_name, template_type):
        """Create a sample template file for a given type."""
        sample_templates = {
            "collection": """# {{ name }} - Agent Collection Specification

> Created: {{ creation_date }}
> Type: Agent Collection
> Status: Draft

## Overview

{{ description }}

## Agents in Collection

{% for agent in agents %}
- **{{ agent.name }}**: {{ agent.description }}
{% endfor %}

## Use Cases

{% for use_case in use_cases %}
- {{ use_case }}
{% endfor %}

## Technical Requirements

- Python compatibility: 3.8+
- Required dependencies: {{ dependencies | join(', ') if dependencies else 'None' }}

## Implementation Plan

{{ implementation_plan | default('TBD') }}
""",
            "agent": """# {{ name }} - Individual Agent Specification

> Created: {{ creation_date }}
> Type: Individual Agent
> Status: Draft

## Role

{{ role }}

## Expertise

{{ expertise }}

## Analysis Focus

{{ analysis_focus }}

## Prompt Template

```
{{ prompt_template | default('# Your specialized analysis prompt goes here...') }}
```

## Integration Points

{{ integration_points | default('To be defined') }}

## Validation Criteria

{{ validation_criteria | default('To be defined') }}
""",
            "integration": """# {{ name }} - Integration Specification

> Created: {{ creation_date }}
> Type: External Integration
> Status: Draft

## System Type

{{ system_type }}

## Integration Method

{{ integration_method }}

## Security Requirements

{{ security_requirements }}

## Data Flow

{{ data_flow | default('To be documented') }}

## Error Handling

{{ error_handling | default('To be documented') }}

## Testing Strategy

{{ testing_strategy | default('To be documented') }}
""",
            "workflow": """# {{ name }} - Workflow Enhancement Specification

> Created: {{ creation_date }}
> Type: Workflow Enhancement
> Status: Draft

## Current Workflow

{{ current_workflow }}

## Proposed Workflow

{{ proposed_workflow }}

## Impact Analysis

{{ impact_analysis }}

## Migration Plan

{{ migration_plan | default('To be developed') }}

## Success Metrics

{{ success_metrics | default('To be defined') }}

## Validation Criteria

{{ validation_criteria | default('To be defined') }}
"""
        }
        
        if template_type not in sample_templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        template_path = self.templates_dir / template_name
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(sample_templates[template_type])
        
        return template_path


def main():
    parser = argparse.ArgumentParser(
        description="Spec Management System - Create, track, and manage feature specifications using Agent OS conventions"
    )
    parser.add_argument(
        '--project-root',
        default='.',
        help='Path to the project root directory (default: current directory)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new specification')
    create_parser.add_argument('--type', required=True, help='Type of spec to create')
    create_parser.add_argument('--name', required=True, help='Name of the specification')
    create_parser.add_argument('--interactive', action='store_true', help='Use interactive mode')
    create_parser.add_argument('--dry-run', action='store_true', help='Preview without creating')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List existing specifications')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--type', help='Filter by type')
    list_parser.add_argument('--format', choices=['table', 'json', 'summary'], 
                           default='table', help='Output format')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Update spec status')
    status_parser.add_argument('--spec', required=True, help='Spec directory name')
    status_parser.add_argument('--status', required=True, help='New status to set')
    status_parser.add_argument('--developer', help='Assign developer')
    status_parser.add_argument('--priority', help='Set priority (low, medium, high)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show detailed spec information')
    info_parser.add_argument('spec', help='Spec directory name')
    
    # Statuses command
    statuses_parser = subparsers.add_parser('statuses', help='List valid statuses and transitions')
    
    # List templates command
    templates_parser = subparsers.add_parser('templates', help='List available templates')
    
    # Init templates command
    init_parser = subparsers.add_parser('init-templates', help='Initialize sample templates')
    init_parser.add_argument('--type', help='Create template for specific type only')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize the spec manager
        spec_manager = SpecManager(args.project_root)
        
        if args.command == 'templates':
            print("Available spec templates:")
            print()
            spec_manager.list_available_templates()
            
            # Also show available template files
            template_files = spec_manager.template_engine.list_available_templates()
            if template_files:
                print(f"\nTemplate files found ({len(template_files)}):")
                for template_file in template_files:
                    print(f"  {template_file}")
            else:
                print("\nNo template files found. Use 'init-templates' to create sample templates.")
        
        elif args.command == 'init-templates':
            template_types = ['collection', 'agent', 'integration', 'workflow']
            
            if args.type:
                if args.type not in template_types:
                    print(f"Error: Unknown template type '{args.type}'")
                    print(f"Available types: {', '.join(template_types)}")
                    sys.exit(1)
                template_types = [args.type]
            
            created_templates = []
            for template_type in template_types:
                template_name = f"{template_type}.md.j2"
                template_path = spec_manager.templates_dir / template_name
                
                if template_path.exists():
                    print(f"Template already exists: {template_name}")
                else:
                    spec_manager.template_engine.create_sample_template(template_name, template_type)
                    created_templates.append(template_name)
                    print(f"✓ Created template: {template_name}")
            
            if created_templates:
                print(f"\nCreated {len(created_templates)} template(s) in {spec_manager.templates_dir}")
            else:
                print("No new templates created (all already exist)")
        
        elif args.command == 'list':
            spec_manager.list_specs(
                status_filter=args.status,
                spec_type_filter=args.type,
                format_output=args.format
            )
        
        elif args.command == 'create':
            # Basic validation
            spec_manager.validate_spec_name(args.name)
            
            if args.type not in spec_manager.templates_config.get("templates", {}):
                print(f"Error: Unknown template type '{args.type}'")
                print("Available templates:")
                spec_manager.list_available_templates()
                sys.exit(1)
            
            spec_dir_name = spec_manager.get_spec_directory_name(args.name)
            
            if spec_manager.spec_exists(spec_dir_name):
                print(f"Error: Spec directory already exists: {spec_dir_name}")
                sys.exit(1)
            
            # Check if template file exists
            template_name = f"{args.type}.md.j2"
            if not spec_manager.template_engine.template_exists(template_name):
                print(f"Error: Template file not found: {template_name}")
                print("Run 'init-templates' to create sample templates.")
                sys.exit(1)
            
            if args.dry_run:
                print(f"Would create spec: {spec_dir_name}")
                print(f"Type: {args.type}")
                print(f"Name: {args.name}")
                print(f"Template: {template_name}")
                
                # Test template rendering with minimal variables
                try:
                    test_variables = {
                        'name': args.name,
                        'creation_date': datetime.now().strftime('%Y-%m-%d'),
                        'description': 'Test description',
                        'agents': [{'name': 'Test Agent', 'description': 'Test agent description'}],
                        'use_cases': ['Test use case 1', 'Test use case 2'],
                        'role': 'Test role',
                        'expertise': 'Test expertise', 
                        'analysis_focus': 'Test analysis focus',
                        'system_type': 'Test system',
                        'integration_method': 'Test method',
                        'security_requirements': 'Test requirements',
                        'current_workflow': 'Current test workflow',
                        'proposed_workflow': 'Proposed test workflow',
                        'impact_analysis': 'Test impact analysis'
                    }
                    rendered = spec_manager.template_engine.render_template(template_name, test_variables, validate_variables=False)
                    print(f"\nTemplate preview (first 300 chars):")
                    print("-" * 50)
                    print(rendered[:300] + "..." if len(rendered) > 300 else rendered)
                    print("-" * 50)
                except Exception as e:
                    print(f"Warning: Template rendering test failed: {e}")
            else:
                print(f"Creating spec: {spec_dir_name}")
                print("Note: Full spec creation will be implemented in Phase 2")
        
        elif args.command == 'status':
            try:
                spec_data = spec_manager.status_tracker.update_spec_status(
                    args.spec, 
                    args.status, 
                    developer=args.developer,
                    priority=args.priority
                )
                print(f"✓ Status updated for {args.spec}")
                print(f"  Status: {spec_data['status']}")
                if spec_data.get('developer'):
                    print(f"  Developer: {spec_data['developer']}")
                if spec_data.get('priority'):
                    print(f"  Priority: {spec_data['priority']}")
                print(f"  Last Updated: {spec_data['last_updated']}")
            except ValueError as e:
                print(f"Error updating status: {e}")
                sys.exit(1)
        
        elif args.command == 'info':
            spec_data = spec_manager.status_tracker.get_spec_details(args.spec)
            if not spec_data:
                print(f"No information found for spec: {args.spec}")
                sys.exit(1)
            
            print(f"Spec: {args.spec}")
            print(f"Name: {spec_data.get('name', 'N/A')}")
            print(f"Type: {spec_data.get('type', 'N/A')}")
            print(f"Status: {spec_data.get('status', 'unknown')}")
            print(f"Priority: {spec_data.get('priority', 'N/A')}")
            print(f"Developer: {spec_data.get('developer', 'unassigned')}")
            print(f"Created: {spec_data.get('created', 'N/A')}")
            print(f"Last Updated: {spec_data.get('last_updated', 'N/A')}")
            
            history = spec_data.get('status_history', [])
            if history:
                print("\nStatus History:")
                for change in history[-5:]:  # Show last 5 changes
                    timestamp = change.get('timestamp', 'N/A')[:19].replace('T', ' ')
                    from_status = change.get('from_status', 'unknown')
                    to_status = change.get('to_status', 'unknown')
                    changed_by = change.get('changed_by', 'unknown')
                    print(f"  {timestamp}: {from_status} → {to_status} (by {changed_by})")
        
        elif args.command == 'statuses':
            print("Valid Statuses:")
            for status in spec_manager.status_tracker.VALID_STATUSES:
                print(f"  {status}")
            
            print("\nStatus Transitions:")
            for from_status, to_statuses in spec_manager.status_tracker.STATUS_TRANSITIONS.items():
                if to_statuses:
                    transitions = ', '.join(to_statuses)
                    print(f"  {from_status} → {transitions}")
                else:
                    print(f"  {from_status} → (final state)")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()