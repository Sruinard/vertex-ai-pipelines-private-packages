#!/bin/bash

# Read config.yaml
python -m pip install pyyaml
eval $(python -c "import yaml;
config = yaml.safe_load(open('config.yaml'));
print(' '.join([f'{k.upper()}={v}' for k,v in config.items()]))")

# Create Google Cloud Artifact Registry
gcloud artifacts repositories create $REPOSITORY \
    --repository-format=python \
    --location=$LOCATION \
    --description="Python repository for airline ML project"

# Create GCS bucket
gsutil mb -l $LOCATION gs://$BUCKET_NAME

# Substitute versions in pyproject.toml and pipeline.py
sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml
sed -i "s|PACKAGE_VERSION=\".*\"|PACKAGE_VERSION=\"$VERSION\"|" airline_ml/pipeline.py
sed -i "s|EXTRA_PIP_INDEX_URL=\".*\"|EXTRA_PIP_INDEX_URL=\"https://$LOCATION-python.pkg.dev/$PROJECT_ID/$REPOSITORY/simple\"|" airline_ml/pipeline.py

# Configure poetry to push to the artifact registry
poetry self update && poetry self add keyrings.google-artifactregistry-auth
poetry config repositories.$REPOSITORY https://$LOCATION-python.pkg.dev/$PROJECT_ID/$REPOSITORY
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
poetry config http-basic.$REPOSITORY oauth2accesstoken $(gcloud auth print-access-token)

# Build and push the package to artifact registry
poetry build
poetry publish -r $REPOSITORY

# Kick off the pipeline
poetry shell
poetry install
poetry run python -m airline_ml.pipeline --config config.yaml


# Reset package version and extra pip index url in pipeline.py to empty strings
sed -i 's|PACKAGE_VERSION=".*"|PACKAGE_VERSION=""|' airline_ml/pipeline.py
sed -i 's|EXTRA_PIP_INDEX_URL=".*"|EXTRA_PIP_INDEX_URL=""|' airline_ml/pipeline.py

echo "Package version and extra pip index URL have been reset to empty strings."

