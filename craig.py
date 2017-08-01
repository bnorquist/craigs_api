import logging

fh = logging.FileHandler(filename='craigs.log')
logging.basicConfig(level=logging.INFO, handlers=fh)
logger = logging.getLogger(__name__)

def record_meta(spider):
    """dynamically fills dictionary with result-meta from each listing"""
    pass

class CraigslistBase(object):
    """ Base class for all Craiglist wrappers. Retrieve all metadata for given filters"""

    def __init__(self):
        self.url
        self.id
        self.title
        self.meta = record_meta()

    url_templates = {
        'base': 'http://{site}.craigslist.org',
        'no_area': 'http://{site}.craigslist.org/search/{category}',
        'area': 'http://{site}.craigslist.org/search/{area}/{category}'
    }

    default_site = 'sfbay'

    default_category = None

    base_filters = {
        'query': {'url_key': 'query', 'value': None},
        'search_titles': {'url_key': 'srchType', 'value': 'T'},
        'has_image': {'url_key': 'hasPic', 'value': 1},
        'posted_today': {'url_key': 'postedToday', 'value': 1},
        'search_distance': {'url_key': 'search_distance', 'value': None},
        'zip_code': {'url_key': 'postal', 'value': None},
    }
    extra_filters = {}

    # Set to True to subclass defines the customize_results() method
    custom_result_fields = False

    sort_by_options = {
        'newest': 'date',
        'price_asc': 'priceasc',
        'price_desc': 'pricedsc',
    }

class CraigslistHousing(CraigslistBase):
