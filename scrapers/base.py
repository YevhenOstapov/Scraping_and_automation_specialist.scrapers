from typing import Union, Dict, Any, Optional
from urllib.parse import urljoin

from parsel import Selector
from requests import Session


class ScraperBase:
    DOMAIN: str = None
    BASE_URL: str = None
    USER_AGENT: str = 'Mozilla/5.0 (X11; Linux x86_64) ' \
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

    def __init__(self):
        self.session: Session = Session()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None,
            selector_params: Optional[Dict[str, Any]] = None) -> Selector:
        response = self.request('GET', path, params=params)
        return Selector(text=response.text, **(dict() if selector_params is None else selector_params))

    def post(self, path: str, payload: Union[Dict[str, Any], str] = None, allow_redirects: bool = False) -> Any:
        return self.request('POST', path, data=payload, allow_redirects=allow_redirects)

    def request(self, method: str, path: str, **kwargs) -> Any:
        if self.BASE_URL is None:
            raise AttributeError('BASE_URL not found')
        if not isinstance(self.session, Session):
            raise TypeError('Attribute session is not Session instance')

        headers = {'user-agent': self.USER_AGENT}
        with self.session as session:
            return session.request(method=method, url=urljoin(self.BASE_URL, path), headers=headers, **kwargs)
