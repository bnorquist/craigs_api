import requests


class scraper(object):

    ## use these to ensure only valid sites and areas are passed into craig.py objects
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