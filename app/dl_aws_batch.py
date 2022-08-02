from .model import get_field_class

import click
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@click.command()
@click.argument(
    "geom_str",
    type=click.STRING
)
@click.argument(
    "fid",
    type=click.STRING
)
@click.argument(
    "s3_bucket",
    type=click.STRING
)
@click.argument(
    "model_name",
    type=click.STRING
)
def run_batch_field_model(
    geom_str,
    fid,
    s3_bucket,
    model_name
):
    geom = json.loads(geom_str)
    result = get_field_class(geom, fid, s3_bucket, model_name)
    logger.info(result)

    return result

if __name__ == "__main__":
    run_batch_field_model()
