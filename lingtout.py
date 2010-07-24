#!/usr/bin/env python
"""Scrapes lingt.com list data with Python

Current canonical location of this module is here:
http://github.com/etrepum/lingtout/tree/master


Usage::

    from lingtout import get_lingt, get_all_lists
    b = get_lingt('YOUR_LINGT_LOGIN', 'YOUR_LINGT_PASSWORD')
    print get_all_lists(b)


"""
# requires simplejson, html5lib
import sys
import pprint
import urllib
import urllib2
import cookielib
from xml.etree import cElementTree

try:
    import simplejson as json
    import html5lib
    from html5lib import treebuilders
except ImportError:
    print >>sys.stderr, """\
lingtout has dependencies::

    html5lib 0.11 http://code.google.com/p/html5lib/
    simplejson 2.1.1 http://code.google.com/p/simplejson/

Try this::

    $ easy_install html5lib simplejson
"""
    raise SystemExit()

__version__ = '0.1'

LOGIN_URL = "http://lingt.com/"
MANAGE_URL = "http://lingt.com/manage/"
LIST_URL = "http://lingt.com/ajax/gettermsfromlistid/"

ETREE_PARSER = html5lib.HTMLParser(
    tree=treebuilders.getTreeBuilder("etree", cElementTree))


def get_lingt(login, password):
    """Returns a twill browser instance after having logged in to lingt
    with *login* and *password*.

    The returned browser will have all of the appropriate cookies set but may
    not be at the exact page that you want data from.

    """
    jar = cookielib.LWPCookieJar()
    b = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    post(b, LOGIN_URL, username=login, password=password).read()
    return b


def post(b, url, **kw):
    """HTTP POST to the url with urlencoded keyword arguments

    """
    return b.open(url, urllib.urlencode(kw))


def get_list_ids(b):
    """Returns the ids of each list in your account.

    """
    doc = ETREE_PARSER.parse(b.open(MANAGE_URL).read())
    return [x.get('id') for x in doc.findall('.//div')
            if x.get('class') == 'lingt-list-entry-container']


def get_list(b, list_id):
    """Returns the json terms for the given list.

    """
    return decode_bad_json(post(b, LIST_URL, id=list_id).read())


def decode_bad_json(data):
    """lingt uses a json encoding that is not standards compliant.

    """
    return json.loads(data.replace("\\'", "'"))


def get_all_lists(b):
    """Return all lists for the current account.

    """
    return dict(
        (list_id, get_list(b, list_id))
        for list_id in get_list_ids(b))

    
def main():
    try:
        login, password = sys.argv[1:]
    except ValueError:
        raise SystemExit("usage: %s LOGIN PASSWORD" % (sys.argv[0],))
    b = get_lingt(login, password)
    obj = get_all_lists(b)
    json.dump(obj, sys.stdout, sort_keys=True, indent='    ', use_decimal=True)
    sys.stdout.write('\n')
    return obj

if __name__ == '__main__':
    data = main()
