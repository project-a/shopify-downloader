"""
Configures access to Shopify API and where to store results
"""


def data_dir() -> str:
    """The directory where result data is written to"""
    return '/tmp/shopify'


def shop_url() -> str:
    """The url of the Shopify shop"""
    return 'myshop.myshopify.com'


def api_key() -> str:
    """The key for accessing the Shopify API access"""
    return '12345a6b7c8d9'


def password() -> str:
    """The password for accessing the Shopify API"""
    return 'mysupersecretpassword'
