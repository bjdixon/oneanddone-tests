#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert

from pages.home import HomePage
from pages.link_crawler import LinkCrawler


class TestHomePage:

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_favicon_present(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        favicon_url = u'%s/%s' % (home_page.base_url, home_page.favicon_url)
        r = requests.get(favicon_url, verify=False)

        Assert.equal(
            r.status_code, 200,
            u'Request to %s responded with %s status code.' % (favicon_url, r.status_code))

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_robots_txt_present(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        robots_url = u'%s/%s' % (home_page.base_url, 'robots.txt')
        r = requests.get(robots_url, verify=False)

        Assert.equal(
            r.status_code, 200,
            u'Request to %s responded with %s status code.' % (robots_url, r.status_code))

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_home_page_links(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        crawler = LinkCrawler(mozwebqa)
        urls = crawler.collect_links(home_page.base_url, **{'class': 'main'})
        bad_urls = []

        Assert.greater(len(urls), 0, u'Something went wrong. No links found.')

        for url in urls:
            check_result = crawler.verify_status_code_is_ok(url)
            if check_result is not True:
                bad_urls.append(check_result)

        Assert.equal(
            0, len(bad_urls),
            u'%s bad links found. ' % len(bad_urls) + ', '.join(bad_urls))
