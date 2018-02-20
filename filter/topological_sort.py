# Copyright (c) 2018 Lars Fenneberg <lf@elemental.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

import collections

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

from ansible import errors

def topological_sort(a, tail_list_key, reverse=False):
    '''Topological sort of a directed acyclic graph'''
    if not HAS_NETWORKX:
        raise errors.AnsibleError('topological_sort(): networkx module is missing')

    if not isinstance(a, collections.Mapping):
        raise errors.AnsibleFilterError('topological_sort(): only works on dictionaries')

    graph = nx.DiGraph()
    
    for head in a.keys():
        # If the value isn't a dictionary or the value doesn't contain our key,
        # just add the key as a node of the graph.
        if not isinstance(a[head], collections.Mapping) or not tail_list_key in a[head]:
            graph.add_node(head)
            continue
    
        if not isinstance(a[head][tail_list_key], list):
            raise errors.AnsibleFilterError('topological_sort(): value of key %s must be a list' % tail_list_key)

        # If the list is empty, just add the key as a node.
        if not a[head][tail_list_key]:
            graph.add_node(head)
            continue
    
        for tail in a[head][tail_list_key]:
            # This implicitly creates the nodes as a side effect.
            graph.add_edge(tail, head)
            
    if not nx.is_directed_acyclic_graph(graph):
        raise errors.AnsibleFilterError('topological_sort(): cycle in graph detected')
        
    return nx.topological_sort(graph, None, reverse)

class FilterModule(object):
    ''' Ansible topological_sort Jinja2 filter '''

    def filters(self):
        filters = {
            'topological_sort': topological_sort,
        }

        return filters
