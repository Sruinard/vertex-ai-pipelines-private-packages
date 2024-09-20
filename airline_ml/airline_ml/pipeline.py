import argparse
import yaml
from google.cloud import aiplatform
from kfp import dsl
from kfp.dsl import component, Input, Output, Dataset
from kfp.compiler import Compiler

# https://LOCATION-python.pkg.dev/PROJECT/REPOSITORY/simple
EXTRA_PIP_INDEX_URL=""
PACKAGE_VERSION=""


@component(
    base_image="python:3.10",
    packages_to_install=[
        f"airline_ml=={PACKAGE_VERSION}",
    ],
    pip_index_urls=[
        EXTRA_PIP_INDEX_URL,
        "https://pypi.org/simple",
    ],
)
def build_airports_dataset_op(output_dataset: Output[Dataset]):
    from airline_ml.business.logic import Dataset, Airport, DatasetRepository

    airports = [
        Airport(name="John F. Kennedy International Airport", country="United States"),
        Airport(name="Los Angeles International Airport", country="United States"),
        Airport(name="O'Hare International Airport", country="United States"),
        Airport(name="Hartsfield-Jackson Atlanta International Airport", country="United States"),
        Airport(name="San Francisco International Airport", country="United States"),
        Airport(name="Heathrow Airport", country="United Kingdom"),
        Airport(name="Tokyo Haneda Airport", country="Japan"),
        Airport(name="Dubai International Airport", country="United Arab Emirates"),
        Airport(name="Charles de Gaulle Airport", country="France"),
        Airport(name="Singapore Changi Airport", country="Singapore"),
        Airport(name="Sydney Airport", country="Australia"),
        Airport(name="Frankfurt Airport", country="Germany"),
        Airport(name="Hong Kong International Airport", country="Hong Kong"),
        Airport(name="Amsterdam Airport Schiphol", country="Netherlands")
    ]

    # Create a Dataset instance and filter American airports
    dataset = Dataset(airports)
    american_airports_dataset = dataset.build()

    # Save the dataset using the repository
    DatasetRepository.save_to_path(american_airports_dataset, output_dataset.path)

@component(
    base_image="python:3.10",
    packages_to_install=[
        f"airline_ml=={PACKAGE_VERSION}",
    ],
    pip_index_urls=[
        EXTRA_PIP_INDEX_URL,
        "https://pypi.org/simple",
    ],
)
def train_model_op(input_dataset: Input[Dataset]):
    from airline_ml.business.logic import DatasetRepository
    from airline_ml.trainer.train import Trainer

    # Load the dataset using the repository
    dataset = DatasetRepository.load_from_path(input_dataset.path)

    # Create a trainer and train the model
    trainer = Trainer(dataset)
    trainer.train(dataset)

    print(f"Total number of samples in the dataset: {len(dataset)}")

@dsl.pipeline(
    name="airport-processing-pipeline",
    description="A pipeline to process airports and train a model",
)
def airport_pipeline():
    dataset_task = build_airports_dataset_op()
    train_model_op(input_dataset=dataset_task.output)

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the airport processing pipeline")
    parser.add_argument("--config", type=str, help="Path to the YAML configuration file")
    args = parser.parse_args()

    if args.config:
        config = load_config(args.config)
        bucket_name = config.get('bucket_name')
        project_id = config.get('project_id')
        location = config.get('location')

    if not bucket_name:
        raise ValueError("Bucket name root must be specified in config file")

    pipeline_root = f"gs://{bucket_name}/pipeline_root"

    # Compile the pipeline
    compiler = Compiler()
    compiler.compile(pipeline_func=airport_pipeline, 
                     package_path="airport_pipeline.json",
                    )

    # Run the pipeline
    aiplatform.init(project=project_id, location=location)
    
    job = aiplatform.PipelineJob(
        display_name="Airport Processing Pipeline",
        template_path="airport_pipeline.json",
        pipeline_root=pipeline_root,
    )
    
    job.submit()

