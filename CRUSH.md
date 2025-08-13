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
- Store Blueprint (.blp) files in elevate/view/blueprints
- Use templates for custom widgets
- Separate UI logic from business logic
- Support multiple languages

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
poetry run pylint elevate/

# Format code
poetry run black elevate/
```

## Github Workflow
Location: ./.github/workflows/build.yml

```yaml
name: Continuous Integration
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened, closed]
  merge_group:
    types: [checks_requested]

concurrency:
  group: ${{ github.workflow }}-${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || github.ref }}
  cancel-in-progress: true

jobs:
  Quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Dependencies
        run: sudo apt update && sudo apt install -y libgirepository1.0-dev libgirepository-2.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          check-latest: true
      - name: Install Python Poetry
        uses: abatilo/actions-poetry@v2.1.0
        with:
          poetry-version: 2.1.3
      - name: Setup poetry to make use of caching
        run: |
          poetry config virtualenvs.create true --local
          poetry config virtualenvs.in-project true --local
      - uses: actions/cache@v4
        name: Define a cache for the virtual environment based on the dependencies lock file
        with:
          path: ./.venv
          key: venv-${{ hashFiles('poetry.lock') }}
      - name: Dependency Install
        run: poetry install --with dev --no-root
      - name: Run Pylint and Black
        run: |
          poetry run black --check src
          poetry run pylint src
      - name: Tests
        run: poetry run python -m pytest -v -s

  Release:
    needs: Quality
    if: (github.event_name == 'pull_request' && github.event.pull_request.merged == true && github.event.pull_request.base.ref == 'main') || (github.event_name == 'merge_group')
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Install Dependencies
        run: sudo apt update && sudo apt install -y libgirepository1.0-dev libgirepository-2.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          check-latest: true
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.PAT }}
      - name: Install Python Poetry
        uses: abatilo/actions-poetry@v2.1.0
        with:
          poetry-version: 2.1.3
      - name: Debug Event Information
        run: |
          echo "Event Name: ${{ github.event_name }}"
          echo "Ref: ${{ github.ref }}"
          echo "Merged: ${{ github.event.pull_request.merged }}"
          echo "Base Ref: ${{ github.event.pull_request.base.ref }}"
      - name: Set Git Credentials
        shell: bash
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
      - name: Setup poetry
        shell: bash
        run: |
          poetry config virtualenvs.create true --local
          poetry config virtualenvs.in-project true --local
      - name: Version and build the package
        shell: bash
        run: |
          poetry version patch
          export APP_VERSION=$(poetry version -s)
          echo "New Version: ${APP_VERSION}"
          sed -i "s/version: '[0-9.]*'/version: '${APP_VERSION}'/" meson.build
          git add pyproject.toml meson.build
          git commit -a -m "chore(release): v${APP_VERSION}"
          git tag v${APP_VERSION}
          git push origin main
          git push origin --tags
```
