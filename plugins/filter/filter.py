#!/usr/bin/python
'''
Author: Nick Russo <njrusmc@gmail.com>

File contains custom filters for use in Ansible playbooks.
https://www.ansible.com/
'''

from __future__ import print_function
import re

class FilterModule(object):
    '''
    Defines a filter module object.
    '''

    @staticmethod
    def filters():
        '''
        Return a list of hashes where the key is the filter
        name exposed to playbooks and the value is the function.
        '''
        return {
            'ios_vrf_rt': FilterModule.ios_vrf_rt,
            'rt_diff': FilterModule.rt_diff
        }

    @staticmethod
    def ios_vrf_rt(text):
        '''
        Parses blocks of VRF text into indexable dictionary entries. This
        typically feeds into the rt_diff function to be tested against the
        intended config.
        '''
        vrf_list = ['vrf' + s for s in text.split('vrf') if s]
        return_dict = {}
        for vrf in vrf_list:
            # Parse the VRF name from the definition line
            name_regex = re.compile(r'vrf\s+definition\s+(?P<name>\S+)')
            name_match = name_regex.search(vrf)
            sub_dict = {}
            vrf_dict = {name_match.group('name'): sub_dict}

            # Parse the RT imports into a list of strings
            rti_regex = re.compile(r'route-target\s+import\s+(?P<rti>\d+:\d+)')
            rti_matches = rti_regex.findall(vrf)
            sub_dict.update({'route_import': rti_matches})

            # Parse the RT exports into a list of strings
            rte_regex = re.compile(r'route-target\s+export\s+(?P<rte>\d+:\d+)')
            rte_matches = rte_regex.findall(vrf)
            sub_dict.update({'route_export': rte_matches})

            # Append dictionary to return list
            return_dict.update(vrf_dict)

        return return_dict


    @staticmethod
    def rt_diff(int_vrf_list, run_vrf_dict):
        '''
        Uses set theory to determine the import/export route-targets that
        should be added or deleted. Only differences are captured, which helps
        Ansible achieve idempotence when making configuration updates.
        '''
        return_list = []
        for int_vrf in int_vrf_list:
            # Copy benign parameters from intended config
            vrf_dict = {
                'name': int_vrf['name'],
                'rd': int_vrf['rd'],
                'description': int_vrf['description']
            }

            # If the intended VRF exists in the running config
            run_vrf = run_vrf_dict.get(int_vrf['name'])
            if run_vrf:
                int_rti = set(int_vrf['route_import'])
                int_rte = set(int_vrf['route_export'])
                run_rti = set(run_vrf['route_import'])
                run_rte = set(run_vrf['route_export'])
                vrf_dict.update({'add_rti': list(int_rti.difference(run_rti))})
                vrf_dict.update({'del_rti': list(run_rti.difference(int_rti))})
                vrf_dict.update({'add_rte': list(int_rte.difference(run_rte))})
                vrf_dict.update({'del_rte': list(run_rte.difference(int_rte))})

            # intended VRF doesn't exist, so add all the RTs
            else:
                vrf_dict.update({'add_rti': int_vrf['route_import']})
                vrf_dict.update({'del_rti': []})
                vrf_dict.update({'add_rte': int_vrf['route_export']})
                vrf_dict.update({'del_rte': []})

            # Add the newly created dictionary to the list of dicts
            return_list.append(vrf_dict)

        return return_list
