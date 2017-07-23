import errno
import gzip
import json
import logging
import shutil
import tempfile
from pathlib import Path

import shopify
from shopify import ShopifyResource

from shopify_downloader import config

OUTPUT_FILE_VERSION = 'v1'


def download_data():
    """Creates a ShopifyApiClient and downloads the data"""
    logger = logging.basicConfig(level=logging.INFO,
                                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    shop_url = "https://{api_key}:{password}@{shopurl}/admin".format(api_key=config.api_key(),
                                                                     password=config.password(),
                                                                     shopurl=config.shop_url())
    shopify.ShopifyResource.set_site(shop_url)
    download_data_sets()


def download_data_sets():
    """Downloads the datasets"""
    for resource in [shopify.Customer, shopify.Product, shopify.Order]:
        download_shopify_resource(resource)


def download_shopify_resource(shopify_resource: ShopifyResource):
    """Downloads data for a single Shopify resource
    https://help.shopify.com/api/reference

    Args:
        shopify_resource:  a Shopify resource e.g Customer, Order, Product

    """

    data = []
    page = 1
    while True:
        resource = shopify_resource.find(limit=250, page=page)
        if len(resource) > 0:
            data.extend(resource)
            page += 1
        else:
            relative_filepath = Path(config.data_dir(),
                                     '{resource_name}-{version}.json.gz'.format(
                                         resource_name=shopify_resource.plural,
                                         version=OUTPUT_FILE_VERSION))
            filepath = ensure_data_directory(relative_filepath)
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_filepath = Path(tmp_dir, relative_filepath)
                tmp_filepath.parent.mkdir(exist_ok=True, parents=True)
                with gzip.open(str(tmp_filepath), 'wt') as tmp_ad_performance_file:
                    tmp_ad_performance_file.write(json.dumps([c.to_dict() for c in data]))
            shutil.move(str(tmp_filepath), str(filepath))
            break


def ensure_data_directory(relative_path: Path = None) -> Path:
    """Checks if a directory in the data dir path exists. Creates it if necessary

    Args:
        relative_path: A Path object pointing to a file relative to the data directory

    Returns:
        The absolute path Path object

    """
    if relative_path is None:
        return Path(config.data_dir())
    try:
        path = Path(config.data_dir(), relative_path)
        # if path points to a file, create parent directory instead
        if path.suffix:
            if not path.parent.exists():
                path.parent.mkdir(exist_ok=True, parents=True)
        else:
            if not path.exists():
                path.mkdir(exist_ok=True, parents=True)
        return path
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
