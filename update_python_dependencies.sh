#!/bin/bash

set -e

# Setup the environment if it doesn't exist
poetry install --no-root

# Generate the requirements.txt file
poetry export --without-hashes --format=requirements.txt > requirements.txt

# Grep through requirements.txt and write matching lines to dev-requirements.txt
#grep -E "$pattern" requirements.txt > dev-requirements.txt
poetry export --only=dev --without-hashes --format=requirements.txt > dev-requirements.txt

# Remove Windows and Darwin requirements
sed -i '/platform_system == "Darwin"/d; /platform_system == "Windows"/d' requirements.txt
sed -i '/platform_system == "Darwin"/d; /platform_system == "Windows"/d' dev-requirements.txt

# NOTE: Req2Flatpak needs to be installed 'locally' because it requires packaging=^21.0 which
# is incompatible with other dependencies.
req2flatpak --requirements-file=dev-requirements.txt --outfile python-build-deps.json --target-platform '312-x86_64'

# Create the Project dependencies
req2flatpak --requirements-file=requirements.txt --outfile python-deps.json --target-platform '312-x86_64'
