# Claude Writing Assistant

A powerful multi-collection writing analysis and improvement system built with [Claude Code](https://claude.ai/code). Get specialized feedback for different writing styles and automatically generate improved versions of your content.

## 🎯 Key Features

- **Multi-Collection Architecture**: Specialized agent sets for different writing styles (fiction, marketing, tutorials, business, technical)
- **Intelligent Analysis**: Expert agents analyze structure, character development, persuasion, clarity, and more
- **Automated Rewriting**: Author agents synthesize all feedback to create improved versions
- **Semantic Versioning**: Track content iterations with automatic version numbering
- **Descriptive Output**: Easy-to-identify directory names (`TIMESTAMP_COLLECTION_FILENAME`)
- **Flexible Workflows**: Run analysis only, full workflow, or rewrite from existing feedback

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/iamseb/claude-writing-assistant.git
cd claude-writing-assistant
./setup.sh

# See available writing collections
python3 scripts/write.py --list-collections

# Try the examples
python3 scripts/write.py inputs/example_story.txt      # Analyze fiction writing
python3 scripts/write.py inputs/marketing_example.txt --collection marketing    # Analyze marketing content
python3 scripts/write.py inputs/tutorial_example.txt --collection tutorial     # Analyze tutorial content
```

## 📚 Writing Collections

### Fiction Writing (Default)
Perfect for stories, novels, and creative writing.
- **Agents**: Structure, Character, Voice, Editing, Consistency
- **Focus**: Narrative flow, character development, prose quality

### Marketing Content
Optimized for ads, copy, and promotional content.
- **Agents**: Persuasion, Audience, Brand Voice, Clarity, Editing
- **Focus**: Conversion optimization, audience targeting, brand consistency

### Tutorial & Educational
Designed for instructional and educational content.
- **Agents**: Instruction Structure, Examples, Clarity, Audience, Editing
- **Focus**: Learning progression, practical examples, clarity

### Business Writing
For professional communications and documents.
- **Agents**: Clarity, Professionalism, Audience, Persuasion, Editing
- **Focus**: Professional tone, clarity, persuasive communication

### Technical Documentation
Specialized for technical docs and specifications.
- **Agents**: Technical Accuracy, Clarity, Instruction Structure, Examples, Editing
- **Focus**: Accuracy, completeness, usability

### Executive Summary
Optimized for C-suite communications and digital transformation presentations.
- **Agents**: Executive Clarity, Strategic Framing, Decision Support, Stakeholder Alignment, Urgency Communication
- **Focus**: Business impact, strategic positioning, executive decision-making

## 💻 Usage

### Basic Commands

```bash
# List all available collections
python3 scripts/write.py --list-collections

# Full workflow (analysis + rewrite) - uses fiction by default
python3 scripts/write.py inputs/your-story.txt

# Specify a collection
python3 scripts/write.py inputs/ad-copy.txt --collection marketing

# Analysis only (no rewrite)
python3 scripts/write.py inputs/content.txt --no-rewrite

# Use specific agents
python3 scripts/write.py inputs/content.txt --collection marketing --agents persuasion clarity
```

### Quick Examples

```bash
python3 scripts/write.py --list-collections        # Show available collections
python3 scripts/write.py inputs/example_story.txt         # Test fiction workflow
python3 scripts/write.py inputs/marketing_example.txt --collection marketing       # Test marketing workflow  
python3 scripts/write.py inputs/tutorial_example.txt --collection tutorial        # Test tutorial workflow
python3 scripts/write.py inputs/executive_test.txt --collection executive         # Test executive workflow
```

### Advanced Workflows

**Rewrite from Existing Analysis:**
```bash
# Generate new rewrite from previous session
python3 scripts/write.py inputs/story.txt --rewrite-only outputs/20250811_143844_fiction_example_story
```

**Custom Agent Selection:**
```bash
# Marketing focus on persuasion and clarity only
python3 scripts/write.py inputs/ad.txt --collection marketing --agents persuasion clarity

# Fiction without consistency checking  
python3 scripts/write.py inputs/story.txt --agents structure character voice editing
```

## 📁 Output Structure

All analyses are saved in descriptively named directories:

```
outputs/
├── 20250811_143728_marketing_ad_copy/
│   ├── persuasion_analysis.md           # Conversion optimization feedback
│   ├── audience_analysis.md             # Target audience insights
│   ├── brand_voice_analysis.md          # Brand consistency review
│   ├── ad_copy_v0.1.0.txt              # Improved rewritten version
│   └── session_summary.json            # Session metadata
│
└── 20250811_143844_fiction_example_story/
    ├── structure_analysis.md           # Plot and pacing feedback
    ├── character_analysis.md           # Character development insights
    ├── voice_analysis.md               # Prose and style feedback
    ├── example_story_v0.2.0.txt        # Improved rewritten version
    └── session_summary.json           # Session metadata
```

**Directory Format**: `TIMESTAMP_COLLECTION_FILENAME`
- Chronological ordering with timestamps
- Clear collection identification
- Easy content identification

## 🛠️ Installation & Setup

### Prerequisites
- **curl** (for Claude Code installation on macOS/Linux)
- **Python 3.6+** (for orchestration script)
- **Claude Code CLI** (installed automatically)

### Installation

```bash
# Option 1: Automated setup
./setup.sh

# Option 2: Manual setup
./setup.sh                    # Install Claude Code CLI
chmod +x scripts/write.py      # Make script executable
```

### Verify Installation

```bash
# Test the system
python3 scripts/write.py inputs/example_story.txt

# Check Claude Code is working
claude --help
```

## 🔧 Configuration

### Agent Collections (`config/agent_collections.json`)

Add new collections or modify existing ones:

```json
{
  "custom_collection": {
    "name": "Custom Writing Style",
    "description": "Your custom analysis approach",
    "analysis_agents": ["agent1", "agent2", "agent3"],
    "author_agent": "custom_author",
    "default": false
  }
}
```

### Custom Agent Prompts

- **Collection-specific**: `prompts/{collection}/{agent}.txt`
- **Shared across collections**: `prompts/shared/{agent}.txt`
- **Author agents**: `prompts/{collection}/{collection}_author.txt`

## 📖 Examples

### Fiction Writing
```bash
python3 scripts/write.py inputs/example_story.txt
```
**Output**: Structure analysis, character development feedback, voice improvements, and a rewritten version with enhanced narrative flow.

### Marketing Copy
```bash
python3 scripts/write.py inputs/marketing_example.txt --collection marketing
```
**Output**: Persuasion optimization, audience targeting insights, brand voice consistency, and conversion-focused rewrite.

### Tutorial Content
```bash
python3 scripts/write.py inputs/tutorial_example.txt --collection tutorial
```
**Output**: Instructional structure analysis, example improvements, clarity enhancements, and learner-optimized rewrite.

### Executive Communications
```bash
python3 scripts/write.py inputs/executive_test.txt --collection executive
```
**Output**: Executive clarity improvements, strategic framing analysis, decision support frameworks, stakeholder alignment guidance, and C-suite appropriate summary.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Add new agent prompts in appropriate collection directories
4. Test with example content
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Adding New Collections

1. Add collection config to `config/agent_collections.json`
2. Create collection directory: `prompts/your_collection/`
3. Add agent prompts and author agent
4. Add example input: `inputs/your_collection_example.txt`
5. Test and document

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Claude Code](https://claude.ai/code) by Anthropic
- Powered by Claude AI for intelligent analysis and rewriting
- Inspired by the need for specialized writing feedback across different domains

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/iamseb/claude-writing-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/iamseb/claude-writing-assistant/discussions)
- **Documentation**: This README and inline code documentation

---

**🤖 Generated with [Claude Code](https://claude.ai/code)**