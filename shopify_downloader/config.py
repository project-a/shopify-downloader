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

def order_status() -> str:
    """Optional argument on order status for retrieving a list of Shopify orders

       open: All open orders (default)
       closed: Show only closed orders
       cancelled: Show only cancelled orders
       any: Any order status
    """
    return 'open'