Simple Akamai API.

Example:

from akamaiapi.api import API

ak = API()

contracts = ak.get('/contract-api/v1/contracts/identifiers?depth=TOP')

