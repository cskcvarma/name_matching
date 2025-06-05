# Contributor Guide

## DEV environment tips
1. uv sync before running the app
2. source venv/bin/activate to activate the environment
3. Install any depeencies needed for your code using the following instructions:
    - uv add <dependency_name> to add a dependency
    - uv remove <dependency_name> to remove a dependency
    - uv add --dev <dependency_name> to add a dev dependency
    - uv remove --dev <dependency_name> to remove a dev dependency
4. Make sure all your code is tested before submitting a PR
5. Test coverage should be above 80%