# Read config.yaml
python -m pip install pyyaml
eval $(python -c "import yaml;
config = yaml.safe_load(open('config.yaml'));
print(' '.join([f'{k.upper()}={v}' for k,v in config.items()]))")


# Substitute versions in pyproject.toml and pipeline.py
sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml
sed -i "s|PACKAGE_VERSION=\".*\"|PACKAGE_VERSION=\"$VERSION\"|" airline_ml/pipeline.py
sed -i "s|EXTRA_PIP_INDEX_URL=\".*\"|EXTRA_PIP_INDEX_URL=\"https://$LOCATION-python.pkg.dev/$PROJECT_ID/$REPOSITORY/simple\"|" airline_ml/pipeline.py


gcloud builds submit --config cloudbuild.yaml \
  --substitutions _PROJECT_ID=$PROJECT_ID,_LOCATION=$LOCATION,_REPOSITORY=$REPOSITORY

# Kick off the pipeline
poetry shell
poetry install
poetry run python -m airline_ml.pipeline --config config.yaml


# Reset package version and extra pip index url in pipeline.py to empty strings
sed -i 's|PACKAGE_VERSION=".*"|PACKAGE_VERSION=""|' airline_ml/pipeline.py
sed -i 's|EXTRA_PIP_INDEX_URL=".*"|EXTRA_PIP_INDEX_URL=""|' airline_ml/pipeline.py

echo "Package version and extra pip index URL have been reset to empty strings."