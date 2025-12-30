# CLI AI Help Specification

**Version:** 1.0.0  
**Status:** Draft  
**Last Updated:** 2025-12-30

## 1. Introduction

This document specifies a standard approach for Command-Line Interface (CLI) tools to provide AI-optimized usage guidance through a dedicated `--ai-help` parameter. As Large Language Models (LLMs) and AI agents increasingly interact with CLI tools, specialized documentation format requirements emerge that differ from traditional human-oriented help text.

### 1.1 Key Words

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## 2. Rationale

### 2.1 Problem Statement

Traditional `--help` output is optimized for human readability with formatting, examples, and concise summaries. AI agents have different needs:

- **Comprehensive date/time format specifications** - AIs commonly make mistakes with date parsing
- **Explicit negative examples** - "Do NOT use X" is clearer than omitting X
- **Error handling guidance** - Common failure modes and solutions
- **Output format recommendations** - Which format is best for programmatic parsing
- **Troubleshooting guides** - Structured error diagnosis
- **Exhaustive option enumeration** - All valid combinations, not just common ones

### 2.2 Benefits

- **Improved AI accuracy** - Reduces hallucination and incorrect command generation
- **Reduced user friction** - AIs can self-serve without iterative trial-and-error
- **Standardization** - Common flag creates predictable discovery pattern
- **Separation of concerns** - Keeps human help concise while providing AI detail

## 3. Specification

### 3.1 Flag Naming

#### 3.1.1 Primary Flag

CLI tools MUST implement the flag `--ai-help`.

**Rationale:** The term "ai-help" is:
- Self-documenting and immediately recognizable
- Clear about audience (AI agents/LLMs)
- Parallel to existing `--help` convention
- Short and memorable

#### 3.1.2 Alternative Names

CLI tools MAY provide aliases such as:
- `--llm-help`
- `--agent-help`
- `--machine-help`

However, `--ai-help` MUST be the primary and documented option.

#### 3.1.3 Deprecated Names

Historical implementations using `--llmhelp` (no hyphen) SHOULD migrate to `--ai-help` to maintain consistency across the ecosystem.

### 3.2 Behavior

#### 3.2.1 Output and Exit

When invoked, the tool MUST:
1. Output the AI-optimized help content to stdout
2. Exit with status code 0
3. Skip all other processing (similar to `--help`)

#### 3.2.2 Eagerness

The `--ai-help` flag SHOULD be processed eagerly, before:
- Credential validation
- API connections
- File system operations
- Other option validation

This allows AIs to learn tool usage without having prerequisite configuration.

### 3.3 Discoverability

#### 3.3.1 Main Help Integration

The CLI tool's primary help text (accessed via `--help` or no arguments) MUST mention the `--ai-help` option prominently. 

RECOMMENDED placement:
```
CLI tool for accessing [service/data].
💡 LLMs/agents: run '[toolname] --ai-help' for detailed usage guidance.
```

#### 3.3.2 Options List

The `--ai-help` flag MUST appear in the options section of standard help output with a description such as:
```
--ai-help    Show comprehensive usage guide for LLMs/agents and exit.
```

#### 3.3.3 No-Argument Behavior

When a user runs the CLI with no arguments or commands, the tool SHOULD display help content that includes mention of `--ai-help`.

### 3.4 Content Requirements

#### 3.4.1 Format

The output MUST be in markdown format with:
- Clear section headers (using `##` and `###`)
- Code blocks with appropriate language tags
- Lists for enumeration
- Emphasis for warnings (e.g., ⚠️, ❌, ✅ emoji)

#### 3.4.2 Required Sections

The help content MUST include:

1. **Overview** - Brief tool description and capabilities
2. **Setup/Prerequisites** - Authentication, installation, configuration
3. **Command Reference** - Complete list of commands/subcommands
4. **Input Specification** - Detailed parameter/argument formats
5. **Output Formats** - Available formats and recommendations
6. **Examples** - Common use cases with actual commands

#### 3.4.3 Recommended Sections

The help content SHOULD include:

1. **Troubleshooting Guide** - Common errors with solutions
2. **Negative Examples** - Explicit "do NOT do this" guidance
3. **Format Conversion Guide** - How to transform common query patterns
4. **Best Practices** - LLM-specific recommendations (e.g., "Always use --json")
5. **Quick Reference Card** - Table of common operations
6. **Error Handling** - Expected failure modes

#### 3.4.4 Date/Time Handling

If the CLI accepts date or time parameters, the documentation MUST:
- List ALL supported formats with examples
- List common UNSUPPORTED formats with explanations
- Provide conversion examples for ambiguous queries
- Include timezone handling guidance

Example:
```markdown
### ✅ SUPPORTED DATE FORMATS
- `2025-12-30` - ISO 8601 date
- `"7 days"` - Relative range

### ❌ UNSUPPORTED FORMATS
- `2025-12-30 to 2025-12-31` - Do NOT use "to" syntax
  Error: "Invalid date specification"
```

#### 3.4.5 Output Format Guidance

For CLIs with multiple output formats, the documentation MUST:
- List all available formats
- Explicitly recommend the best format for programmatic consumption
- Warn against formats that are difficult to parse

Example:
```markdown
⚠️ **LLM Best Practice: Always Use --json**

✅ RECOMMENDED for programmatic analysis:
    tool fetch --json

❌ NOT RECOMMENDED for parsing:
    tool fetch --tree
```

#### 3.4.6 Error Examples

The documentation SHOULD include:
- Actual error messages the tool produces
- Root cause explanations
- Corrected command examples

Example:
```markdown
### Error: "Got unexpected extra argument"
**Cause:** Multiple arguments without proper quoting

❌ WRONG: tool fetch 2025-01-01 2025-01-31
✅ CORRECT: tool fetch "2025-01-01 30 days"
```

### 3.5 Content Style

#### 3.5.1 Verbosity

AI help content SHOULD be more verbose than human help. Explicit is better than concise.

#### 3.5.2 Tone

Content SHOULD:
- Be direct and imperative
- Use active voice
- Avoid ambiguity
- Repeat important information if needed

#### 3.5.3 Visual Markers

Content SHOULD use emoji or symbols to highlight:
- ✅ Correct examples
- ❌ Incorrect examples  
- ⚠️ Important warnings
- 💡 Tips and best practices
- 🔧 Troubleshooting steps

## 4. Implementation Guidance

### 4.1 File vs. Inline

Implementations MAY either:
1. Store help content in a separate markdown file (e.g., `docs/ai-help.md`)
2. Embed content inline in source code

RECOMMENDED approach: Separate markdown file for easier maintenance and version control.

### 4.2 Maintenance

The AI help content SHOULD:
- Be updated whenever command syntax changes
- Include version information or date stamp
- Be reviewed by both humans and AIs during testing
- Track common AI mistakes and address them in documentation

### 4.3 Testing

Implementers SHOULD:
- Test that `--ai-help` exits without side effects
- Verify markdown renders correctly in common tools
- Validate that examples are copy-paste executable
- Test with actual AI agents to identify gaps

### 4.4 Examples by Framework

#### 4.4.1 Python (Click)
```python
@click.command()
@click.option('--ai-help', is_flag=True, is_eager=True, 
              help='Show AI/LLM usage guide and exit')
def cli(ai_help):
    if ai_help:
        click.echo(load_ai_help())
        raise SystemExit(0)
```

#### 4.4.2 Python (Typer)
```python
def ai_help_callback(value: bool) -> None:
    if value:
        typer.echo(show_ai_help())
        raise typer.Exit()

@app.callback()
def main(
    ai_help: bool = typer.Option(
        False, "--ai-help",
        callback=ai_help_callback,
        is_eager=True,
        help="Show AI/LLM usage guide"
    )
): ...
```

#### 4.4.3 Go (Cobra)
```go
var aiHelpFlag bool

func init() {
    rootCmd.PersistentFlags().BoolVar(&aiHelpFlag, 
        "ai-help", false, 
        "Show AI/LLM usage guide and exit")
}

func Execute() {
    if aiHelpFlag {
        fmt.Println(getAIHelp())
        os.Exit(0)
    }
    rootCmd.Execute()
}
```

## 5. Evolution and Versioning

### 5.1 Specification Versioning

This specification uses semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Incompatible changes to flag name or behavior
- MINOR: New recommended sections or practices
- PATCH: Clarifications and examples

### 5.2 Content Versioning

Individual CLI tools MAY version their AI help content. RECOMMENDED format:
```markdown
# Tool Name AI Help Guide
**Version:** 2.1.0
**Last Updated:** 2025-12-30
```

## 6. Security Considerations

### 6.1 Information Disclosure

AI help content SHOULD NOT include:
- API keys, tokens, or credentials (even examples)
- Internal system paths beyond necessary examples
- Sensitive business logic or rate limits
- Security vulnerabilities or known exploits

### 6.2 Injection Risks

If AI help content is dynamically generated:
- Input MUST be sanitized
- Template injection MUST be prevented
- Content SHOULD be static when possible

## 7. Future Considerations

### 7.1 Machine-Readable Format

Future versions MAY specify:
- JSON schema for structured help content
- OpenAPI-like command specifications
- Formal grammar definitions for inputs

### 7.2 Interactive Mode

Future versions MAY specify:
- `--ai-help interactive` for Q&A mode
- Structured queries (e.g., `--ai-help dates`)
- Multi-language support

## 8. References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) - Key words for use in RFCs
- [CommonMark](https://commonmark.org/) - Markdown specification
- [CLI Guidelines](https://clig.dev/) - General CLI best practices
- [GNU Standards for CLIs](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)

## 9. Acknowledgments

This specification is informed by:
- Real-world LLM interactions with CLI tools
- Common patterns in AI agent error logs
- User feedback on AI-generated command suggestions
- The OuraCLI reference implementation

## Appendix A: Complete Example

See OuraCLI's implementation:
- Flag definition: `src/ouracli/cli.py`
- Help content: `src/ouracli/llm_help.py`
- User-facing result: `ouracli --ai-help`

Key features demonstrated:
- Prominent discoverability in main help
- Comprehensive date format documentation with negative examples
- Output format recommendations for AI parsing
- Troubleshooting guide with actual error messages
- Quick reference card for common operations
- Explicit best practices for LLMs

## Appendix B: Implementation Checklist

- [ ] Add `--ai-help` flag to CLI
- [ ] Make flag eager (processes before other validation)
- [ ] Output markdown-formatted content to stdout
- [ ] Exit with code 0 after output
- [ ] Include all required sections (§3.4.2)
- [ ] Mention `--ai-help` in main help text
- [ ] Add `--ai-help` to options list
- [ ] Document all date/time formats if applicable
- [ ] Provide output format recommendations
- [ ] Include error examples with solutions
- [ ] Use visual markers (✅, ❌, ⚠️, 💡)
- [ ] Test with actual AI agent
- [ ] Validate examples are executable
- [ ] Review for information disclosure
- [ ] Add version/date to content
