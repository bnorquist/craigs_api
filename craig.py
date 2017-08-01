import logging
from bs4 import BeautifulSoup
import requests

fh = logging.FileHandler(filename='craigs.log')
logging.basicConfig(level=logging.INFO, handlers=fh)
logger = logging.getLogger(__name__)

def record_meta(spider):
    """dynamically fills dictionary with result-meta from each listing"""
    pass

class CraigslistBase(object):
    """ Base class for all Craiglist wrappers. Retrieve all metadata for given filters"""

    def __init__(self, site=None, area=None, category=None, filters=None):

        #self.url
        #self.id
        #self.title
        self.sites_url = 'http://www.craigslist.org/about/sites'
        self.all_sites = self.get_all_sites()
        self.meta = record_meta()
        self.category = category

        if self.site not in self.all_sites:
            msg = "{} is not a valid site".format(self.site)
            logger.error(msg)
            raise ValueError(msg)
        self.site = site

        if area:
            if not self.is_valid_area(area):
                msg = "'%s' is not a valid area for site '%s'" % (area, site)
                self.logger.error(msg)
                raise ValueError(msg)
        self.area = area


    def is_valid_area(self, area):
        """Check if area is valid"""
        base_url = self.url_templates['base']
        response = requests.get(base_url.format({'site': self.site}))
        soup = BeautifulSoup(response.content, 'html.parser')
        sublinks = soup.find('ul', {'class': 'sublinks'})
        return sublinks and sublinks.find('a', text=area) is not None

    def get_all_sites(self):
        response = requests.get(self.sites_url)
        response.raise_for_status()  # Something failed?
        soup = BeautifulSoup(response.content, 'html.parser')
        sites = set()

        for box in soup.findAll('div', {'class': 'box'}):
            for a in box.findAll('a'):
                # Remove protocol and get subdomain
                site = a.attrs['href'].rsplit('//', 1)[1].split('.')[0]
                sites.add(site)

        return sites

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
