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

    def __init__(self, site, area=None, category=None, filters=None):
        self.sites_url = 'http://www.craigslist.org/about/sites'
        self.url_templates = {
                                'base': 'http://{site}.craigslist.org',
                                'no_area': 'http://{site}.craigslist.org/search/{category}',
                                'area': 'http://{site}.craigslist.org/search/{area}/{category}'
                            }
        self.base_filters = {
                                'query': {'url_key': 'query', 'value': None},
                                'search_titles': {'url_key': 'srchType', 'value': 'T'},
                                'has_image': {'url_key': 'hasPic', 'value': 1},
                                'posted_today': {'url_key': 'postedToday', 'value': 1},
                                'search_distance': {'url_key': 'search_distance', 'value': None},
                                'zip_code': {'url_key': 'postal', 'value': None},
                            }

        self.site = self.is_valid_site(site)
        self.area = [self.is_valid_area(area) if area is not None else None]
        self.category = category

    def is_valid_area(self, area):
        """Check if area is valid and exists"""
        base_url = self.url_templates['base']
        response = requests.get(base_url.format({'site': self.site}))
        soup = BeautifulSoup(response.content, 'html.parser')
        sublinks = soup.find('ul', {'class': 'sublinks'})
        if sublinks and sublinks.find('a', text=area) is not None:
            return area
        else:
            msg = "{} is not a valid area for site {}".format(area, self.site)
            logger.error(msg)
            raise ValueError(msg)

    def is_valid_site(self, site):
        """Check if site is valid and exists"""
        all_sites = self.get_all_sites()
        if site in all_sites:
            logger.info('valid site detected ({})'.format(site))
            return site
        else:
            logger.debug('site not valid ({})'.format(site))

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

    def create_request(self):
        url_template = self.url_templates['area' if self.area is not None else 'no_area']
        url_settings = {'site': self.site, 'area': self.area, 'category': self.category}
        # construct url with input parameters
        url = url_template.format(**url_settings)

        response = requests.get(url=url, params=self.filters)
        logger.debug("Craig's response: {}".format(response.url))
        logger.debug("Craig's status code: {}".format(response.status_code))

    # implement later if needed
    # self.sort_by_options = {
    #     'newest': 'date',
    #     'price_asc': 'priceasc',
    #     'price_desc': 'pricedsc',
    # }
    # self.meta = record_meta()

class CraigslistHousing(CraigslistBase):
    pass
