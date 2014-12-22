# -*- coding: utf-8 -*-
"""A Sphinx extension for linking to your project's issue tracker."""
from docutils import nodes, utils

__version__ = '0.1.0'


def user_role(name, rawtext, text, lineno,
              inliner, options=None, content=None):
    """Sphinx role for linking to a user profile. Defaults to linking to
    Github profiles, but the profile URIS can be configured via the
    ``issues_user_uri`` config value.

    Example: ::

        :user:`sloria`
    """
    options = options or {}
    content = content or []
    username = utils.unescape(text).strip()
    config = inliner.document.settings.env.app.config
    if config.issues_user_uri:
        ref = config.issues_user_uri.format(user=username)
    else:
        ref = 'https://github.com/{0}'.format(username)
    text = '@{0}'.format(username)
    link = nodes.reference(text=text, refuri=ref, **options)
    return [link], []


def _make_issue_node(issue_no, config, options=None):
    options = options or {}
    if issue_no not in ('-', '0'):
        if config.issues_uri:
            ref = config.issues_uri.format(issue=issue_no)
        elif config.issues_github_path:
            ref = 'https://github.com/{0}/issues/{1}'.format(
                config.issues_github_path, issue_no
            )
        issue_text = '#{0}'.format(issue_no)
        link = nodes.reference(text=issue_text, refuri=ref, **options)
    else:
        link = None
    return link


def issue_role(name, rawtext, text, lineno,
               inliner, options=None, content=None):
    """Sphinx role for linking to an issue. Must have
    `issues_uri` or `issues_github_path` configured in ``conf.py``.

    Examples: ::

        :issue:`123`
        :issue:`42,45`
    """
    options = options or {}
    content = content or []
    issue_nos = [each.strip() for each in utils.unescape(text).split(',')]
    config = inliner.document.settings.env.app.config
    ret = []
    for i, issue_no in enumerate(issue_nos):
        node = _make_issue_node(issue_no, config, options=options)
        ret.append(node)
        if i != len(issue_nos) - 1:
            sep = nodes.raw(text=', ', format='html')
            ret.append(sep)
    return ret, []


def setup(app):
    # Format template for issues URI
    # e.g. 'https://github.com/sloria/marshmallow/issues/{issue}
    app.add_config_value('issues_uri', default=None, rebuild='html')
    # Shortcut for Github, e.g. 'sloria/marshmallow'
    app.add_config_value('issues_github_path', default=None, rebuild='html')
    # Format template for user profile URI
    # e.g. 'https://github.com/{user}'
    app.add_config_value('issues_user_uri', default=None, rebuild='html')
    app.add_role('issue', issue_role)
    app.add_role('user', user_role)
