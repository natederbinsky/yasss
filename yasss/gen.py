from typing import Any, Callable, Iterable, Mapping, Tuple, Union
from typing_extensions import Literal

from sys import stderr
from os import makedirs, path, walk
from shutil import rmtree, copyfile

from jinja2 import Environment, PrefixLoader, PackageLoader, FileSystemLoader, select_autoescape # type: ignore


def eprint(msg: str) -> None:
    """Utility function for error output."""
    print(msg, file=stderr)


def clean(destination: str) -> None:
    """Removes a supplied directory recursively."""
    if path.exists(destination) and path.isdir(destination):
        rmtree(destination)


def build(templ_name: str, templ_dir: str, site_dir: str, destination: str, pages: Iterable[str]=(), templ_resources: Iterable[Union[str, Tuple[str, Callable[[str, str], bool]]]]=(), site_resources: Iterable[Union[str, Tuple[str, Callable[[str, str], bool]]]]=(), templ_data: Mapping[str, Any]={}, site_data: Mapping[str, Any]={}, globals: Mapping[str, Any]={}) -> Literal[True]:
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

    def resource_copy(s_fname: str, d_fname: str) -> None:
        makedirs(path.dirname(d_fname), exist_ok=True)
        copyfile(s_fname, d_fname)
    
    def resource_walk(s_dir: str, prefix: str, filter_f: Callable[[str, str], bool]) -> None:
        for root, dirs, files in walk(s_dir):
            for fname in files:
                rel_path = root[len(prefix)+1:]
                if filter_f(rel_path, fname):
                    resource_copy(path.join(root, fname), _dest(path.join(rel_path, fname)))
    
    def _source_templ(s: str) -> str:
        return path.join(templ_dir, s)

    def _source_site(s: str) -> str:
        return path.join(site_dir, s)

    def _dest(s: str) -> str:
        return path.join(destination, s)

    #

    for r in templ_resources:
        if isinstance(r, str):
            resource_copy(_source_templ(r), _dest(r))
        else:
            resource_walk(_source_templ(r[0]), templ_dir, r[1])

    for r in site_resources:
        if isinstance(r, str):
            resource_copy(_source_site(r), _dest(r))
        else:
            resource_walk(_source_site(r[0]), site_dir, r[1])

    return True
