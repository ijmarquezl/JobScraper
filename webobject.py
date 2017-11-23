#!/usr/bin/python3
"""Object that retrieves and manages the html information from the web page."""

from requests import get
from bs4 import BeautifulSoup as BS


class WebObject:
    """Class that makes a functionality abstraction for web operations."""

    __page = ""
    __soup = ""

    def __init__(self):
        """Object initialization."""
        pass

    def getURLContents(self, url):
        """Retrieve the HTML code for a particular webpage."""
        self.__page = get(url)
        self.__soup = BS(self.__page.text, 'html.parser')
        return self.__page.status_code

    @property
    def page(self):
        """Get the page of a web site."""
        return self.__page

    @page.setter
    def page(self, page):
        """Set the page of the web site."""
        self.__page = page

    @property
    def soup(self):
        """Get the Soup contents."""
        return self.__soup

    def getByClass(self, clsname):
        """Recover an array of all the elements with a class name."""
        return self.__soup.find_all(class_=clsname)

    def getByDiv(self, attributes, s):
        """Recover an array of all the div elements with an attribute."""
        return s.find_all(name='div', attrs=attributes)

    def getByA(self, attributes, s):
        """Recover an array of a labels with an attribute in particular."""
        return s.find_all(name='a', attrs=attributes)

    def getBySpan(self, attributes, s):
        """Recover an array of span labels with an attribute."""
        return s.find_all('span', attrs=attributes)

    def find(self, attributes, s, clsname=None):
        """Find a specific attribute in a soup."""
        if clsname is None:
            return s.find(attributes)
        else:
            return s.find(name=clsname, attrs=attributes)
