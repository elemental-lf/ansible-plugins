# Copyright (c) 2018 Lars Fenneberg <lf@elemental.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

# https://github.com/asottile/dockerfile or pip install dockerfile
try:
    import dockerfile
    HAS_DOCKERFILE = True
except ImportError:
    HAS_DOCKERFILE = False

from six import raise_from
from ansible import errors
from ansible.plugins.lookup import LookupBase
from ansible.utils.listify import listify_lookup_plugin_terms

class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):
        if not HAS_DOCKERFILE:
            raise errors.AnsibleError('dockerfile module is missing')
            
        terms[1] = listify_lookup_plugin_terms(terms[1], templar=self._templar, loader=self._loader)
        terms[1] = map(lambda cmd: unicode(cmd.lower()), terms[1])

        if not isinstance(terms, list) or not len(terms) == 2:
            raise errores.AnsibleError('dockerfile_search lookup expect a list of two items');

        try:
            df = dockerfile.parse_string(unicode(terms[0]))
        except (dockerfile.GoIOError, dockerfile.GoParseError) as e:
            if isinstance(e, dockerfile.GoIOError):
                raise_from(errors.AnsibleError("Dockerfile couldn't be opened"), e)
            else:
                raise_from( errors.AnsibleError("Dockerfile couldn't be parsed"), e)

        return [command._asdict() for command in df if command.cmd in terms[1]]
