# Database Schema

This is the database schema implementation for the spec detailed in @.agent-os/specs/2025-08-14-spec-management-system/spec.md

> Created: 2025-08-14
> Version: 1.0.0

## Schema Changes

### Spec Status Database (`config/spec_status.json`)

```json
{
  "specs": {
    "2025-08-14-spec-management-system": {
      "id": "2025-08-14-spec-management-system",
      "name": "Spec Management System",
      "type": "workflow",
      "status": "draft",
      "priority": "high",
      "created_date": "2025-08-14",
      "updated_date": "2025-08-14",
      "assigned_developer": null,
      "estimated_effort": "2 weeks",
      "actual_effort": null,
      "tags": ["agent-os", "cli", "development-workflow"],
      "dependencies": [],
      "related_specs": [],
      "completion_percentage": 0,
      "tasks": {
        "total": 0,
        "completed": 0,
        "in_progress": 0
      },
      "metadata": {
        "phase": "Phase 1: Agent OS Integration",
        "roadmap_item": true,
        "breaking_changes": false
      }
    }
  },
  "status_definitions": {
    "draft": {
      "description": "Specification is being written and reviewed",
      "next_states": ["approved", "rejected"]
    },
    "approved": {
      "description": "Specification approved for implementation",
      "next_states": ["in-progress", "draft"]
    },
    "in-progress": {
      "description": "Implementation has started",
      "next_states": ["complete", "blocked", "draft"]
    },
    "blocked": {
      "description": "Implementation blocked by dependencies",
      "next_states": ["in-progress", "draft"]
    },
    "complete": {
      "description": "Implementation completed and deployed",
      "next_states": []
    },
    "rejected": {
      "description": "Specification rejected, will not be implemented",
      "next_states": ["draft"]
    }
  },
  "type_definitions": {
    "collection": {
      "description": "New agent collection for writing analysis",
      "template": "collection.md.j2",
      "default_priority": "medium"
    },
    "agent": {
      "description": "Individual analysis or author agent",
      "template": "agent.md.j2", 
      "default_priority": "medium"
    },
    "integration": {
      "description": "External system or tool integration",
      "template": "integration.md.j2",
      "default_priority": "low"
    },
    "workflow": {
      "description": "Development workflow or process enhancement",
      "template": "workflow.md.j2",
      "default_priority": "high"
    }
  }
}
```

### Template Configuration (`config/spec_templates.json`)

```json
{
  "templates": {
    "collection": {
      "template_file": "templates/specs/collection.md.j2",
      "required_fields": ["name", "description", "agents", "use_cases"],
      "optional_fields": ["dependencies", "examples"],
      "validation_rules": {
        "name": "^[a-z][a-z0-9-]*$",
        "agents": "min_length:2"
      }
    },
    "agent": {
      "template_file": "templates/specs/agent.md.j2", 
      "required_fields": ["name", "role", "expertise", "analysis_focus"],
      "optional_fields": ["specialized_knowledge", "output_format"],
      "validation_rules": {
        "name": "^[a-z][a-z0-9-]*$",
        "role": "min_length:10"
      }
    },
    "integration": {
      "template_file": "templates/specs/integration.md.j2",
      "required_fields": ["name", "external_system", "integration_type", "data_flow"],
      "optional_fields": ["authentication", "rate_limits"],
      "validation_rules": {
        "name": "^[a-z][a-z0-9-]*$",
        "integration_type": "enum:api,webhook,file,database"
      }
    },
    "workflow": {
      "template_file": "templates/specs/workflow.md.j2",
      "required_fields": ["name", "current_workflow", "proposed_workflow", "benefits"],
      "optional_fields": ["migration_plan", "training_requirements"],
      "validation_rules": {
        "name": "^[a-z][a-z0-9-]*$"
      }
    }
  },
  "global_variables": {
    "project_name": "Claude Writing Assistant",
    "agent_os_version": "1.0.0",
    "default_author": "Development Team"
  }
}
```

## Migrations

### Migration 1: Initial Schema Creation

**File**: `config/spec_status.json`
**Action**: Create initial database file with empty specs collection and schema definitions

```python
def migrate_initial_schema():
    """Create initial spec status database."""
    initial_data = {
        "specs": {},
        "status_definitions": {...},  # As defined above
        "type_definitions": {...}     # As defined above
    }
    
    with open('config/spec_status.json', 'w') as f:
        json.dump(initial_data, f, indent=2)
```

### Migration 2: Template Configuration

**File**: `config/spec_templates.json`  
**Action**: Create template configuration file with validation rules and field definitions

```python
def migrate_template_config():
    """Create template configuration file."""
    template_config = {...}  # As defined above
    
    with open('config/spec_templates.json', 'w') as f:
        json.dump(template_config, f, indent=2)
```

### Migration 3: Template Directory Structure

**Action**: Create template directory and initial Jinja2 templates

```python
def migrate_template_files():
    """Create template directory structure and files."""
    os.makedirs('templates/specs', exist_ok=True)
    
    # Create each template file with Agent OS-compliant structure
    templates = ['collection.md.j2', 'agent.md.j2', 'integration.md.j2', 'workflow.md.j2']
    for template in templates:
        create_template_file(f'templates/specs/{template}')
```