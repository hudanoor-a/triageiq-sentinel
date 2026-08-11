import boto3
import yaml
import click
import logging
import os


def setup_logging(log_file, level):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def load_config(config_path):
    with open(config_path) as f:
        return yaml.safe_load(f)


def create_bucket(s3_client, bucket_name, region, logger):
    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        logger.info(f"Bucket created: {bucket_name}")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        logger.info(f"Bucket already exists: {bucket_name}")


def upload_dataset(s3_client, local_path, bucket_name, s3_key, logger):
    logger.info(f"Uploading {local_path} to s3://{bucket_name}/{s3_key}")
    s3_client.upload_file(local_path, bucket_name, s3_key)
    logger.info(f"Upload complete: s3://{bucket_name}/{s3_key}")


@click.command()
@click.option('--config', default='config.yaml', help='Path to config file')
@click.option('--upload', is_flag=True, help='Upload dataset to S3')
def main(config, upload):
    cfg = load_config(config)
    logger = setup_logging(
        cfg['logging']['log_file'],
        cfg['logging']['level']
    )

    logger.info("Pipeline started")
    logger.info(f"Loaded config from {config}")

    if upload:
        s3 = boto3.client('s3', region_name=cfg['aws']['region'])
        create_bucket(s3, cfg['aws']['bucket_name'], cfg['aws']['region'], logger)
        upload_dataset(
            s3,
            cfg['dataset']['local_path'],
            cfg['aws']['bucket_name'],
            cfg['dataset']['s3_key'],
            logger
        )

    logger.info("Pipeline finished")


if __name__ == '__main__':
    main()
