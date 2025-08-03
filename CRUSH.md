# Elevate Project CRUSH Configuration

## Build Commands
```bash
# Build project
foundry build

# Run project
foundry run

# Clean project
foundry clean 

# Update python dependencies
poetry update && ./update_python_dependencies.sh
```

## Code Style Guidelines
- Follow Python PEP 8 style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 105 characters
- Use descriptive variable and function names
- Use type hints where possible
- Use Google-style docstrings for modules, classes, methods, and functions
- Follow GNOME Human Interface Guidelines for UI elements
- Use GTK4 and Libadwaita for mobile aware UI components

## Import Organization
- Standard library imports first
- Third-party imports second
- Local imports last
- Separate import groups with blank line
- Use explicit imports (no wildcard imports)

## Naming Conventions
- Classes: PascalCase
- Functions/variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Private members: prefixed with underscore

## Error Handling
- Use try/except blocks appropriately
- Prefer specific exceptions over broad except clauses
- Log errors with appropriate context
- Use custom/subclassed exceptions where appropriate

## UI Development
- Use Blueprint (.blp) files for complex layouts
- Store Blueprint (.blp) files in src/view/blueprints
- Use templates for custom widgets
- Separate UI logic from business logic

## Testing
```bash
# Run all tests (if available)
poetry run pytest

# Run specific test (replace with actual test command if available)
poetry run pytest tests/test_specific.py::test_function
```

## Linting
```bash
# Check for style issues
poetry run pylint src/

# Format code
poetry run black src/
```
