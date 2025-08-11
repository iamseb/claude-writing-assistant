# Writing Assistant with Claude Code Sub-Agents

A comprehensive writing analysis system that uses specialized Claude Code sub-agents to provide targeted feedback for different types of writing - from creative fiction to marketing copy to technical documentation.

## Project Structure

```
writer/
├── agents/             # Individual agent directories (optional, for future use)
│   ├── structure/
│   ├── character/
│   ├── voice/
│   ├── editing/
│   └── consistency/
├── prompts/            # System prompts for each sub-agent
│   ├── structure.txt
│   ├── character.txt
│   ├── voice.txt
│   ├── editing.txt
│   └── consistency.txt
├── inputs/             # Input files to be analyzed
│   └── example_story.txt
├── outputs/            # Generated analysis reports (timestamped sessions)
├── scripts/            # Orchestration scripts
│   └── write.py
└── README.md
```

## Writing Collections

The system supports different collections of specialized agents for various writing styles:

### Available Collections

**Fiction** (default): Creative writing analysis
- Structure, Character, Voice, Editing, Consistency agents
- Author agent optimized for narrative improvement

**Marketing**: Marketing content optimization  
- Persuasion, Audience, Clarity, Brand Voice, Editing agents
- Author agent focused on conversion optimization

**Tutorial**: Educational content enhancement
- Instruction Structure, Clarity, Audience, Examples, Editing agents  
- Author agent specialized in learning effectiveness

**Business**: Professional communication
- Clarity, Professionalism, Audience, Persuasion, Editing agents

**Technical**: Technical documentation
- Technical Accuracy, Clarity, Instruction Structure, Examples, Editing agents

## Agent Details

### Structure Agent (`prompts/structure.txt`)
- Analyzes narrative structure and pacing
- Evaluates story architecture (three-act, hero's journey, etc.)
- Identifies plot holes and structural weaknesses
- Suggests improvements to dramatic tension and flow

### Character Agent (`prompts/character.txt`)
- Focuses on character development and authenticity
- Analyzes character arcs and motivations
- Evaluates dialogue for voice distinctiveness
- Reviews character relationships and dynamics

### Voice & Tone Agent (`prompts/voice.txt`)
- Maintains consistent narrative voice
- Evaluates prose style and rhythm
- Ensures appropriate tone for genre and audience
- Balances showing vs. telling

### Editing Agent (`prompts/editing.txt`)
- Provides developmental and copy editing
- Corrects grammar, syntax, and style issues
- Improves clarity and readability
- Eliminates redundancies and awkward passages

### Consistency Agent (`prompts/consistency.txt`)
- Tracks continuity across all story elements
- Identifies contradictions in plot, character, and setting
- Ensures adherence to established story world rules
- Maintains terminology and naming consistency

### Author Agent (`prompts/author.txt`)
- **Master rewriter** that synthesizes all specialist feedback
- Creates improved versions incorporating analysis recommendations
- Maintains original story essence while implementing improvements
- Generates semantically versioned output files (e.g., `story_v0.1.0.txt`)
- Balances competing suggestions for optimal narrative impact

## Usage

### Prerequisites
- Python 3.6+
- Claude Code CLI installed and configured

### Basic Usage

Analyze a text file with all agents:
```bash
python3 scripts/write.py inputs/example_story.txt
```

Analyze with specific agents only:
```bash
python3 scripts/write.py inputs/marketing_example.txt --collection marketing --agents persuasion clarity
```

Specify a different project root:
```bash
python scripts/write.py /path/to/input.txt --project-root /path/to/writer/project
```

### Output

The script creates descriptively named session directories in `outputs/` with format `TIMESTAMP_COLLECTION_FILENAME`:
- Individual analysis files for each agent (e.g., `structure_analysis.md`)
- `session_summary.json` with metadata and results

Example output structure:
```
outputs/
└── session_20241201_143022/
    ├── structure_analysis.md
    ├── character_analysis.md
    ├── voice_analysis.md
    ├── editing_analysis.md
    ├── consistency_analysis.md
    └── session_summary.json
```

### Example Workflow

1. Place your writing content in the `inputs/` directory
2. Run the analysis script:
   ```bash
   python scripts/write.py inputs/my_story.txt
   ```
3. Review the generated analyses in the `outputs/TIMESTAMP_COLLECTION_FILENAME/` directory
4. Apply the feedback to improve your writing
5. Re-run analysis to track improvements

### Customizing Agents

To modify an agent's behavior, edit the corresponding prompt file in `prompts/`:
- `structure.txt` - Narrative structure specialist
- `character.txt` - Character development specialist  
- `voice.txt` - Voice and tone specialist
- `editing.txt` - Developmental and copy editor
- `consistency.txt` - Consistency and continuity specialist

## Tips

- Start with structural analysis before detailed editing
- Use the consistency agent throughout longer works
- Run voice analysis when switching between chapters or sections
- The editing agent works best on relatively polished drafts
- Consider running agents incrementally rather than all at once for large works

## Troubleshooting

- Ensure Claude Code CLI is properly installed and configured
- Check that input files exist and are readable
- Verify that all prompt files are present in the `prompts/` directory
- Review session summary JSON for specific agent errors