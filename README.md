[![Build Status](
https://travis-ci.org/nickrusso42518/vpnm.svg?branch=master)](
https://travis-ci.org/nickrusso42518/vpnm)

# MPLS L3VPN Manager (vpnm)
This playbook is true infrastructure-as-code. Users declare a list of VRFs
under Ansible's control, then specify which route-targets should exist.
Any unspecified route-targets are automatically and idempotently removed.
Whenever changes occur, routing and ping reachability is validated.

> Contact information:\
> Email:    njrusmc@gmail.com\
> Twitter:  @nickrusso42518

  * [Supported platforms](#supported-platforms)
  * [Variables](#variables)
  * [Task summary](#task-summary)

## Supported platforms
At present, only Cisco IOS platforms are supported.

Testing was conducted on the following platforms and versions:
  * Cisco CSR1000v, version 16.08.01a, running in AWS

```
$ cat /etc/redhat-release
Red Hat Enterprise Linux Server release 7.4 (Maipo)

$ uname -a
Linux ip-10-125-0-100.ec2.internal 3.10.0-693.el7.x86_64 #1 SMP
  Thu Jul 6 19:56:57 EDT 2017 x86_64 x86_64 x86_64 GNU/Linux

$ ansible --version
ansible 2.6.2
  config file = /home/ec2-user/natm/ansible.cfg
  configured module search path = [u'/home/ec2-user/.ansible/plugins/modules',
    u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, May  3 2017, 07:55:04)
    [GCC 4.8.5 20150623 (Red Hat 4.8.5-14)]
```

## Variables
For each host (or group of hosts), a `vrf` list is defined. This list of
dictionaries has the following format:

```
---
vrfs:
  - name: '1'
    description: "first VRF"
    rd: "65000:1"
    route_import:
      - "65000:1"
    route_export:
      - "65000:2"
    check:
      routes:
        - "10.3.3.0/30"
        - "10.4.4.0/24"
      pings:
        - "10.3.3.1"
        - "10.4.4.44"
  - name: '2'
    description: "second VRF"
    rd: "65000:2"
    route_import:
      - "65000:1"
    route_export:
      - "65000:2"
    check:
      routes:
        - "10.3.3.0/30"
        - "10.4.4.0/24"
      pings:
        - "10.3.3.1"
        - "10.4.4.44"
```

The individual components in each dictionary are as follows:
  * `name`: The name of the VRF. Numbers can be used, but should be quoted
    as strings to prevent type mismatches later.
  * `description`: The description of the VRF.
  * `rd`: The BGP route distinguisher that makes all routes in this VRF
    unique from the perspective of BGP.
  * `route_import`: The list of route target (RT) extended communities,
    ideally quoted as strings, which should be imported. Any import RTs not
    in this list that are present on the target host are removed.
  * `route_export`: The list of route target (RT) extended communities,
    ideally quoted as strings, which should be exported. Any export RTs not
    in this list that are present on the target host are removed.
  * `check`: Optional nested dictionary that helps with verification. To
    disable checking entirely, remove this dictionary or set it to `false`.
      * `routes`: List of prefixes in CIDR notation which should be present
        in the VRF FIB (CEF table) after RT changes are made. This ensures
        that the configuration actually work, and may help surface unrelated
        issues, such as a BGP VPN route advertisement problem.
      * `pings`: List of single IP addreses which should be pinged from
        within the VRF. Often this will be an IP from inside one of the
        prefixes specified in the `routes` key, but it does not have to be.
        This helps surface reachability problems or routing loops.

## Task summary
The playbook begins by collecting the existing VRF configuration and parsing
it to retrieve the currently configured import and export RTs for all VRFs
on the router, even those not being managed by this playbook. Next, the
parsed RT information from the router is compared against the user-provided
intended RT configuration. For each user-defined VRF, the playbook determines
which RTs must be added or deleted. RTs absent from the intended RT
configuration are automatically and idempotently removed. The playbook also
ensures that each VRF is defined as a BGP AFI and redistributes any connected
routes. If a user-defined VRF does not exist in the current configuration, it
is added, along with all defined RTs. If a VRF exists in the current
configuration but does not exist in the user-defined configuration, it is
ignored. This conservative behavior allows some VRFs to remain outside of
Ansible's control (for example, a management VRF).

If any changes were made, the system waits for a configurable amount of time,
with a default of 60 seconds. This allows the router to import new routes into
the VRF and affix new exported RTs. It also accounts for the time needed for
VRF FIBs to install their routes upon receipt from BGP. The system also
prints the changes made to stdout. When there are no changes, there is no
wait period and no stdout output.

Last, the routing and ping verification runs. These test cases are run
regardless of whether changes occurred or not.

Please see the outputs in the `samples/` directory to see the playbook output.
