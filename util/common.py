import urllib
from urlparse import urlparse

def url_idna_quote(url):
	protocol, domain, path, params, query, fragment = urlparse(url)
	domain = unicode(domain, 'utf-8', 'ignore')
	domain = domain.encode('idna')
	if path is None:
		path = ''
	else:
		path = urllib.quote_plus(path, safe='=&?/')
	return domain + path


def url_pyu_quote(url):
    protocol, domain, path, params, query, fragment = urlparse(url)
    domain = domain.decode('idna')
    if path is None:
        path = ''
    else:
        path = urllib.quote_plus(path, safe='=&?/')
    return domain + path
