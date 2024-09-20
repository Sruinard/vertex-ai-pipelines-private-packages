# Airline ML Pipeline

This project demonstrates how to set up and run a machine learning pipeline for airline data processing using Google Cloud's Vertex AI Pipelines and Artifact Registry.

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and configured
- Python 3.10 or later
- Poetry package manager

## Setup

1. Clone this repository and navigate to the project directory.

2. Copy the `example_config.yaml` to `config.yaml` and fill in your specific details:

   ```yaml
   bucket_name: your-gcs-bucket-name
   project_id: your-gcp-project-id
   location: your-preferred-region
   repository: your-artifact-registry-repo-name
   version: your-package-version
   ```

3. Install the required Python packages:

   ```bash
   pip install poetry pyyaml
   ```

## Running the Application

1. Run the setup script to prepare the environment and start the Cloud Build process:

   ```bash
   ./setup.sh
   ```

   This script will:
   - Read the configuration from `config.yaml`
   - Update version information in `pyproject.toml` and `pipeline.py`
   - Submit the build job to Cloud Build

2. After the Cloud Build job completes, run the pipeline:

   ```bash
   ./cloudbuild.sh
   ```

   This script will:
   - Read the configuration from `config.yaml`
   - Submit the build job to Cloud Build
   - Install the package and run the pipeline
   - Reset version information in `pipeline.py`

## Project Structure

- `airline_ml/`: Main package directory
  - `pipeline.py`: Contains the Vertex AI pipeline definition
- `cloudbuild.yaml`: Cloud Build configuration file
- `config.yaml`: Project configuration file
- `setup.sh`: Setup script for initializing the project
- `cloudbuild.sh`: Script to run Cloud Build and the pipeline

## Notes

- Ensure that your Google Cloud project has the necessary APIs enabled (Vertex AI, Artifact Registry, Cloud Build).
- Make sure your GCP account has the required permissions to create and manage resources.
- The `VERSION` in `config.yaml` should be updated for each new release of your package.

## Troubleshooting

If you encounter any issues:
- Check your `config.yaml` file for correct values
- Ensure you have the necessary permissions in your GCP project
- Review the Cloud Build logs for any error messages

For more detailed information about each component, refer to the comments in the individual script files.