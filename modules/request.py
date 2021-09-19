# This file contains the function that makes requests on behalf of the application, essentially a wrapper around requests.

import requests as rq

def makeGetRequest(url, params, cookies, auth, hdrs, timeout):

    craftedUrl = url + params

    req = rq.get(craftedUrl, headers, cookies, auth, hdrs)

    return req


def makePOSTRequest(url, data, cookies, auth, timeout, hdrs):
    craftedUrl = url + params

    req = rq.post(url,data=data)

    return req