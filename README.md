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
Coming soon

## Task summary
Coming soon
