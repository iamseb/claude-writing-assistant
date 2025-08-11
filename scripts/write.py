#!/usr/bin/env python3
"""
Writing Assistant Orchestrator
Coordinates multiple Claude Code sub-agents for comprehensive writing analysis and improvement.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class WritingOrchestrator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.prompts_dir = self.project_root / "prompts"
        self.outputs_dir = self.project_root / "outputs"
        self.config_dir = self.project_root / "config"
        
        # Load agent collections configuration
        self.collections = self.load_collections()
        self.default_collection = self.get_default_collection()
        
        # Ensure output directory exists
        self.outputs_dir.mkdir(exist_ok=True)
    
    def load_collections(self):
        """Load agent collections from configuration file."""
        config_file = self.config_dir / "agent_collections.json"
        if not config_file.exists():
            raise FileNotFoundError(f"Agent collections config not found: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_default_collection(self):
        """Get the default collection name."""
        for name, config in self.collections.items():
            if config.get('default', False):
                return name
        return list(self.collections.keys())[0]  # fallback to first collection
    
    def get_collection_agents(self, collection_name):
        """Get analysis agents and author agent for a collection."""
        if collection_name not in self.collections:
            raise ValueError(f"Unknown collection: {collection_name}. Available: {list(self.collections.keys())}")
        
        config = self.collections[collection_name]
        return config['analysis_agents'], config['author_agent']
    
    def list_collections(self):
        """List available collections with descriptions."""
        for name, config in self.collections.items():
            default_marker = " (default)" if config.get('default', False) else ""
            print(f"{name}{default_marker}: {config['description']}")
    
    def create_session_dir_name(self, timestamp, collection_name, input_file):
        """Create a descriptive session directory name."""
        input_name = Path(input_file).stem
        # Clean up the input name to be filesystem-safe
        clean_input_name = re.sub(r'[^a-zA-Z0-9_-]', '_', input_name)[:30]  # Limit length
        return f"{timestamp}_{collection_name}_{clean_input_name}"
    
    def load_prompt(self, agent_name, collection_name):
        """Load the system prompt for a specific agent in a collection."""
        # Try collection-specific prompt first
        collection_prompt = self.prompts_dir / collection_name / f"{agent_name}.txt"
        if collection_prompt.exists():
            with open(collection_prompt, 'r', encoding='utf-8') as f:
                return f.read().strip()
        
        # Fall back to shared prompt
        shared_prompt = self.prompts_dir / "shared" / f"{agent_name}.txt"
        if shared_prompt.exists():
            with open(shared_prompt, 'r', encoding='utf-8') as f:
                return f.read().strip()
        
        raise FileNotFoundError(f"Prompt file not found for agent '{agent_name}' in collection '{collection_name}' or shared directory")
    
    def load_input(self, input_file):
        """Load the input content to be analyzed."""
        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def create_agent_prompt(self, agent_name, system_prompt, user_content):
        """Create a combined prompt for the agent."""
        return f"""System: {system_prompt}

User: Please analyze the following content according to your specialized role:

{user_content}

Provide detailed feedback and specific suggestions for improvement."""
    
    def create_author_prompt(self, system_prompt, original_content, feedback_files):
        """Create a prompt for the author agent with all specialist feedback."""
        feedback_content = ""
        for feedback_file in feedback_files:
            if feedback_file.exists():
                agent_name = feedback_file.stem.replace('_analysis', '')
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    feedback_content += f"\n\n## {agent_name.upper()} SPECIALIST FEEDBACK:\n{f.read()}"
        
        return f"""System: {system_prompt}

User: Please rewrite the following text by incorporating the feedback from all specialist agents. Focus on creating an improved version that addresses the key issues while maintaining the original's essence.

ORIGINAL TEXT:
{original_content}

SPECIALIST FEEDBACK:{feedback_content}

Provide only the rewritten text - no explanations or commentary."""
    
    def run_claude_agent(self, agent_name, prompt, output_file):
        """Run Claude Code for a specific agent."""
        print(f"Running {agent_name} agent...")
        
        try:
            # Run claude with the prompt using --print mode for non-interactive output
            # Pass prompt directly as argument instead of file
            result = subprocess.run([
                'claude',
                '--print',
                prompt
            ], capture_output=True, text=True, check=True)
            
            # Write output to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            print(f"✓ {agent_name} analysis complete")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error running {agent_name} agent: {e}")
            print(f"stderr: {e.stderr}")
            return False
    
    def get_next_version(self, input_file):
        """Generate semantic version for the rewritten file."""
        input_path = Path(input_file)
        base_name = input_path.stem
        extension = input_path.suffix
        
        # Look for existing versions in outputs
        version_pattern = re.compile(rf"{re.escape(base_name)}_v(\d+)\.(\d+)\.(\d+){re.escape(extension)}$")
        highest_version = (0, 0, 0)
        
        for session_dir in self.outputs_dir.glob('*'):
            for file in session_dir.glob(f"{base_name}_v*{extension}"):
                match = version_pattern.match(file.name)
                if match:
                    version = tuple(map(int, match.groups()))
                    if version > highest_version:
                        highest_version = version
        
        # Increment minor version (for improvements)
        major, minor, patch = highest_version
        new_version = (major, minor + 1, patch)
        
        return f"{base_name}_v{new_version[0]}.{new_version[1]}.{new_version[2]}{extension}"
    
    def run_analysis_agents(self, input_file, collection_name=None, agents=None):
        """Run analysis agents only."""
        if collection_name is None:
            collection_name = self.default_collection
        
        collection_analysis_agents, _ = self.get_collection_agents(collection_name)
        
        if agents is None:
            agents = collection_analysis_agents
        else:
            # Validate that specified agents are available in the collection
            invalid_agents = set(agents) - set(collection_analysis_agents)
            if invalid_agents:
                print(f"Warning: The following agents are not available in collection '{collection_name}': {invalid_agents}")
                agents = [a for a in agents if a in collection_analysis_agents]
        
        # Load input content
        try:
            content = self.load_input(input_file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return False, None
        
        # Create descriptive output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir_name = self.create_session_dir_name(timestamp, collection_name, input_file)
        session_dir = self.outputs_dir / session_dir_name
        
        session_dir.mkdir(exist_ok=True)

        print(f"Starting writing analysis session: {timestamp}")
        print(f"Collection: {collection_name} ({self.collections[collection_name]['name']})")
        print(f"Input: {input_file}")
        print(f"Output directory: {session_dir}")
        print(f"Analysis agents: {', '.join(agents)}")
        print()
        
        results = {}
        feedback_files = []
        
        for agent_name in agents:
            try:
                # Load agent's system prompt
                system_prompt = self.load_prompt(agent_name, collection_name)
                
                # Create combined prompt
                full_prompt = self.create_agent_prompt(agent_name, system_prompt, content)
                
                # Set output file
                output_file = session_dir / f"{agent_name}_analysis.md"
                feedback_files.append(output_file)
                
                # Run the agent
                success = self.run_claude_agent(agent_name, full_prompt, output_file)
                results[agent_name] = {
                    'success': success,
                    'output_file': str(output_file)
                }
                
            except FileNotFoundError as e:
                print(f"Error with {agent_name}: {e}")
                results[agent_name] = {'success': False, 'error': str(e)}
        
        return results, (session_dir, feedback_files, content, collection_name)
    
    def run_author_agent(self, session_dir, feedback_files, original_content, input_file, collection_name):
        """Run the author agent to create a rewritten version."""
        print(f"\nRunning author agent for rewriting...")
        
        try:
            # Get author agent for collection
            _, author_agent = self.get_collection_agents(collection_name)
            
            # Load author system prompt
            system_prompt = self.load_prompt(author_agent, collection_name)
            
            # Create author prompt with all feedback
            full_prompt = self.create_author_prompt(system_prompt, original_content, feedback_files)
            
            # Generate version filename
            version_filename = self.get_next_version(input_file)
            output_file = session_dir / version_filename
            
            # Run the author agent
            success = self.run_claude_agent(author_agent, full_prompt, output_file)
            
            if success:
                print(f"✓ Rewritten version saved as: {version_filename}")
                return {'success': True, 'output_file': str(output_file), 'version': version_filename}
            else:
                return {'success': False}
                
        except FileNotFoundError as e:
            print(f"Error with author agent: {e}")
            return {'success': False, 'error': str(e)}
    
    def run_full_workflow(self, input_file, collection_name=None, agents=None, rewrite=True):
        """Run complete workflow: analysis + optional rewriting."""
        # Run analysis agents
        analysis_results, session_data = self.run_analysis_agents(input_file, collection_name, agents)
        
        if not analysis_results:
            return False
        
        session_dir, feedback_files, original_content, collection_name = session_data
        all_results = analysis_results.copy()
        
        # Run author agent if requested
        if rewrite:
            author_result = self.run_author_agent(session_dir, feedback_files, original_content, input_file, collection_name)
            _, author_agent = self.get_collection_agents(collection_name)
            all_results[author_agent] = author_result
        
        # Create summary file
        summary_file = session_dir / "session_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': session_dir.name.split('_')[0],
                'session_name': session_dir.name,
                'collection': collection_name,
                'input_file': str(input_file),
                'workflow': 'full' if rewrite else 'analysis_only',
                'agents_run': list(all_results.keys()),
                'results': all_results
            }, f, indent=2)
        
        print(f"\nSession complete. Results saved in: {session_dir}")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Writing Assistant Orchestrator - Coordinate Claude Code sub-agents for writing analysis"
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Path to the input file containing content to analyze'
    )
    parser.add_argument(
        '--collection', '-c',
        help='Writing collection to use (default: fiction). Use --list-collections to see available options'
    )
    parser.add_argument(
        '--agents',
        nargs='+',
        help='Specific analysis agents to run (default: all agents in collection)'
    )
    parser.add_argument(
        '--no-rewrite',
        action='store_true',
        help='Run analysis only, skip author rewrite agent'
    )
    parser.add_argument(
        '--rewrite-only',
        help='Path to existing session directory to run author agent on existing feedback'
    )
    parser.add_argument(
        '--list-collections',
        action='store_true',
        help='List available writing collections and exit'
    )
    parser.add_argument(
        '--project-root',
        default='.',
        help='Path to the project root directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = WritingOrchestrator(args.project_root)
    
    # Handle list collections command
    if args.list_collections:
        print("Available writing collections:")
        print()
        orchestrator.list_collections()
        sys.exit(0)
    
    # Require input file for all other operations
    if not args.input_file:
        parser.error('input_file is required unless using --list-collections')
    
    # Handle different workflow modes
    if args.rewrite_only:
        # Rewrite mode: use existing session feedback
        session_path = Path(args.rewrite_only)
        if not session_path.exists():
            print(f"Error: Session directory not found: {session_path}")
            sys.exit(1)
        
        # Load original content and feedback files
        try:
            original_content = orchestrator.load_input(args.input_file)
            feedback_files = list(session_path.glob('*_analysis.md'))
            
            # Determine collection from session summary if available
            collection_name = args.collection or orchestrator.default_collection
            summary_file = session_path / 'session_summary.json'
            if summary_file.exists():
                with open(summary_file, 'r') as f:
                    summary = json.load(f)
                    collection_name = summary.get('collection', collection_name)
            else:
                # Try to extract collection from directory name (format: TIMESTAMP_COLLECTION_FILENAME)
                dir_parts = session_path.name.split('_')
                if len(dir_parts) >= 3 and dir_parts[1] in orchestrator.collections:
                    collection_name = dir_parts[1]
            
            author_result = orchestrator.run_author_agent(session_path, feedback_files, original_content, args.input_file, collection_name)
            success = author_result['success']
        except Exception as e:
            print(f"Error in rewrite mode: {e}")
            success = False
    else:
        # Normal workflow
        rewrite = not args.no_rewrite
        success = orchestrator.run_full_workflow(args.input_file, args.collection, args.agents, rewrite)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()