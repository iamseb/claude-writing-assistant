# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-08-14-spec-management-system/spec.md

> Created: 2025-08-14
> Version: 1.0.0

## Endpoints

### CLI Command Interface

#### Create Spec
```bash
python scripts/spec.py create [OPTIONS]
```

**Options:**
- `--type, -t`: Spec type (collection, agent, integration, workflow) [required]
- `--name, -n`: Spec name (kebab-case) [required]
- `--interactive, -i`: Use interactive prompt mode [default: true]
- `--template`: Custom template file path [optional]
- `--dry-run`: Preview spec without creating files [optional]

**Examples:**
```bash
python scripts/spec.py create -t collection -n sales-proposal
python scripts/spec.py create --type workflow --name batch-processing --interactive
```

#### List Specs
```bash
python scripts/spec.py list [OPTIONS]
```

**Options:**
- `--status, -s`: Filter by status (draft, approved, in-progress, complete, blocked, rejected) [optional]
- `--type, -t`: Filter by type (collection, agent, integration, workflow) [optional]
- `--format, -f`: Output format (table, json, summary) [default: table]
- `--sort`: Sort by field (date, name, status, priority) [default: date]

**Examples:**
```bash
python scripts/spec.py list --status in-progress
python scripts/spec.py list --type collection --format json
```

#### Update Status
```bash
python scripts/spec.py status [OPTIONS]
```

**Options:**
- `--spec, -s`: Spec identifier [required]
- `--status`: New status value [required]
- `--developer`: Assign developer [optional]
- `--priority`: Update priority (low, medium, high, critical) [optional]
- `--notes`: Add status change notes [optional]

**Examples:**
```bash
python scripts/spec.py status -s 2025-08-14-spec-management-system --status approved
python scripts/spec.py status --spec sales-proposal --status in-progress --developer john.doe
```

#### Task Management
```bash
python scripts/spec.py tasks [OPTIONS]
```

**Options:**
- `--spec, -s`: Spec identifier [required]
- `--generate, -g`: Generate tasks from spec content [optional]
- `--list, -l`: List current tasks [default]
- `--complete`: Mark task as complete [optional]
- `--add`: Add new task [optional]

**Examples:**
```bash
python scripts/spec.py tasks -s 2025-08-14-spec-management-system --generate
python scripts/spec.py tasks --spec sales-proposal --complete "implement basic collection structure"
```

#### Validation
```bash
python scripts/spec.py validate [OPTIONS]
```

**Options:**
- `--spec, -s`: Spec identifier (or --all for all specs) [required]
- `--fix`: Attempt to fix common issues [optional]
- `--strict`: Use strict validation rules [optional]

**Examples:**
```bash
python scripts/spec.py validate -s 2025-08-14-spec-management-system
python scripts/spec.py validate --all --fix
```

## Controllers

### SpecManager Controller

```python
class SpecManager:
    """Main controller for spec management operations."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.specs_dir = project_root / '.agent-os' / 'specs'
        self.config_dir = project_root / 'config'
        self.templates_dir = project_root / 'templates' / 'specs'
        
        # Load configurations
        self.status_db = self.load_status_database()
        self.templates_config = self.load_templates_config()
    
    def create_spec(self, spec_type: str, name: str, **kwargs) -> Dict:
        """Create new specification from template."""
        
    def list_specs(self, status: str = None, spec_type: str = None) -> List[Dict]:
        """List specifications with optional filtering."""
        
    def update_status(self, spec_id: str, status: str, **metadata) -> bool:
        """Update specification status and metadata."""
        
    def validate_spec(self, spec_id: str, strict: bool = False) -> Dict:
        """Validate specification against rules."""
        
    def generate_tasks(self, spec_id: str) -> List[Dict]:
        """Generate task list from specification content."""
```

### TemplateEngine Controller

```python
class TemplateEngine:
    """Handle template loading and rendering."""
    
    def __init__(self, templates_dir: Path, config: Dict):
        self.templates_dir = templates_dir
        self.config = config
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
    
    def render_template(self, template_name: str, variables: Dict) -> str:
        """Render template with provided variables."""
        
    def validate_template_variables(self, template_name: str, variables: Dict) -> List[str]:
        """Validate required template variables are present."""
        
    def list_templates(self) -> List[Dict]:
        """List available templates with metadata."""
```

### StatusTracker Controller

```python
class StatusTracker:
    """Handle spec status and lifecycle management."""
    
    def __init__(self, status_file: Path):
        self.status_file = status_file
        self.data = self.load_status_data()
    
    def update_spec_status(self, spec_id: str, status: str, metadata: Dict = None) -> bool:
        """Update spec status with validation."""
        
    def get_spec_status(self, spec_id: str) -> Dict:
        """Get current status and metadata for spec."""
        
    def validate_status_transition(self, current_status: str, new_status: str) -> bool:
        """Validate if status transition is allowed."""
        
    def get_specs_by_status(self, status: str) -> List[Dict]:
        """Get all specs with specified status."""
```

### CLI Controller

```python
class SpecCLI:
    """Command-line interface controller."""
    
    def __init__(self):
        self.spec_manager = SpecManager(Path('.'))
        self.parser = self.setup_argument_parser()
    
    def setup_argument_parser(self) -> argparse.ArgumentParser:
        """Configure CLI argument parser."""
        
    def handle_create_command(self, args) -> None:
        """Handle spec creation command."""
        
    def handle_list_command(self, args) -> None:
        """Handle spec listing command."""
        
    def handle_status_command(self, args) -> None:
        """Handle status update command."""
        
    def handle_tasks_command(self, args) -> None:
        """Handle task management command."""
        
    def handle_validate_command(self, args) -> None:
        """Handle spec validation command."""
```