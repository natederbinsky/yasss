from typing import Any, Iterable, Mapping
from typing_extensions import Literal

from sys import stderr
from os import makedirs, path
from shutil import rmtree, copyfile

from jinja2 import Environment, PrefixLoader, PackageLoader, FileSystemLoader, select_autoescape # type: ignore


def eprint(msg: str) -> None:
    """Utility function for error output."""
    print(msg, file=stderr)


def clean(destination: str) -> None:
    """Removes a supplied directory recursively."""
    if path.exists(destination) and path.isdir(destination):
        rmtree(destination)


def build(templ_name: str, templ_dir: str, site_dir: str, destination: str, pages: Iterable[str]=(), templ_resources: Iterable[str]=(), site_resources: Iterable[str]=(), templ_data: Mapping[str, Any]={}, site_data: Mapping[str, Any]={}, globals: Mapping[str, Any]={}) -> Literal[True]:
    """Generic function to build a site given a template.

    First, removes the destination folder and creates an
    empty folder in its place.

    Then integrates Jinja files from the template with site
    pages and renders them using template/site data into
    the destination.

    Finally, copies template and site resources to the
    destination.

    Return is always True; calling functions may preempt
    via custom parameter validation.
    """

    ###
    # Remove/create the destination folder
    ###

    clean(destination)
    makedirs(destination)

    ###
    # Render page templates
    ###

    SITEPREFIX = '_site'

    env = Environment(
        extensions=['jinja2_highlight.HighlightExtension'],
        loader=PrefixLoader({
            templ_name: FileSystemLoader(templ_dir),
            SITEPREFIX: FileSystemLoader(site_dir)
        }),
        autoescape=select_autoescape(enabled_extensions=('htm', 'html'))
    )
    env.globals.update(**globals)

    for fname in pages:        
        env.get_template('{}/{}'.format(SITEPREFIX, fname)) \
        .stream(_tdata=templ_data, data=site_data) \
        .dump(path.join(destination, fname))

    ###
    # Copy static resources
    ###

    def resource_copy(fname: str, templ_resource: bool) -> None:
        s_fname = path.join(templ_dir if templ_resource else site_dir, fname)

        d_fname = path.join(destination, fname)
        makedirs(path.dirname(d_fname), exist_ok=True)

        copyfile(s_fname, d_fname)
    

    for fname in templ_resources:
        resource_copy(fname, True)

    for fname in site_resources:
        resource_copy(fname, False)

    return True
