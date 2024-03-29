from __future__ import annotations

import logging
import requests

from . import auth
from . import query

logger = logging.getLogger(__name__)


class Opendatasoft:
  def __init__(
    self,
    subdomain: str = 'data',
    base_url: str = None,
    session: requests.Session = None,
    api_key: str = None,
    lang: str = 'en',
    timezone: str = 'UTC'
  ) -> None:
    """
    :param subdomain: Subdomain used to create the base API URL,
      eg. https://{subdomain}.opendatasoft.com. Default: `data`, (the hub for
      all public datasets in Opendatasoft's network)
    :param base_url: Custom base API URL
    :param session: A session object with which to make API calls
    :param api_key: Opendatasoft API key for accessing private datasets
    :param lang: Language used to format strings (for example, in the
      `date_format` method)
    :param timezone: Timezone applied to datetime fields in queries and
      responses
    """
    self.base_url = (
      base_url.strip('/')
      if base_url
      else f'https://{subdomain}.opendatasoft.com'
    )
    self.session = session or requests.Session()
    if api_key:
      self.login(api_key)

    self.catalog = query.CatalogQuery(
      api_options={
        'base_url': self.base_url,
        'session': self.session
      },
      lang=lang,
      timezone=timezone
    )

  def login(self, api_key: str) -> None:
    """Login to an Opendatasoft domain to access private datasets."""
    self.session.auth = auth.TokenAuth(api_key)
