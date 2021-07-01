from typing import Any, Iterable, Mapping, Optional, Union

from pygments import highlight # type: ignore
from pygments.lexers import get_lexer_by_name # type: ignore
from pygments.formatters import HtmlFormatter # type: ignore
from markupsafe import Markup # type: ignore
import base64

def code(source: str, lexer: Union[str, Any], formatOpts: Mapping[str, Any] = {}) -> Markup:
    """Creates highlighted source code. 
    
    Based upon a lexer name (or instance) and formatter options
    """
    return Markup(highlight(
        source,
        get_lexer_by_name(lexer) if isinstance(lexer, str) else lexer,
        HtmlFormatter(**formatOpts)
    ))


def inline_img(type: str, b64_data: Optional[bytes]=None, img_fname: str=None, attrs: Mapping[str, str]={}) -> Markup:
    """Creates an image tag for inline representation. 
    
    Requires its type (e.g., png, gif), either base64 data or file name, 
    and optional attributes
    """
    if (b64_data and img_fname) or (not b64_data and not img_fname):
        return None

    if not b64_data and img_fname:
        with open(img_fname, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read())

    return Markup('<img src="data:image/{};base64, {}" {}/>'.format(
        type, b64_data.decode('ascii'), # type: ignore
        "" if not attrs else '{} '.format(' '.join(['{}="{}"'.format(k, v) for k,v in attrs.items()]))))


def link(url: str, text: Optional[str]=None, new_window: bool=True, title: str="") -> Markup:
    """Creates an anchor tag targeted to a new window

    Provides for the ability to override the link text,
    title, and whether it's in a new window.
    """
    return Markup('<a href="{}"{} title="{}">{}</a>'.format(
        url,
        ' target="_blank"' if new_window else '',
        title,
        text if text else url
    ))


def email(address: str, text: Optional[str]=None, title: str="") -> Markup:
    """Creates an e-mail anchor.

    Provides for the ability to override the link text and title
    """
    return link('mailto:{}'.format(address), text if text else address, title=title)


def lst(items: Iterable[str], ordered: bool) -> Markup:
    """Creates a list of items, ordered or not."""
    return Markup('<{sep}>{contents}</{sep}>'.format(sep='ol' if ordered else 'ul', contents=''.join('<li>{}</li>'.format(el) for el in items)))


def ulist(*items: str) -> Markup:
    """Creates an unordered list of items supplied as arguments."""
    return lst(items=items, ordered=False)


def olist(*items: str) -> Markup:
    """Creates an ordered list of items supplied as arguments."""
    return lst(items=items, ordered=True)
