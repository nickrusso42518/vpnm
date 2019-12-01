Existing device configuration has problems when compared to
`../host_vars/csr1.yml` which is the intended state.

```
# VRF has an extra export RT 1:1
vrf definition VRF1
 description first VRF
 rd 65000:1
 route-target export 65000:2
 route-target export 1:1
 route-target import 65000:1

# VRF is missing the import RT 65000:1
vrf definition VRF2
 description second VRF
 rd 65000:2
 route-target export 65000:2

# VRF has an extra export RT 1:1
# VRF is missing the import RT 65000:2
vrf definition VRF3
 description third VRF
 rd 65000:3
 route-target export 65000:1
 route-target export 1:1
```

Running the playbook reveals and corrects these problems.

```
$ ansible-playbook vpnm_playbook.yml

PLAY [Manage MPLS L3VPN route-targets] ****************************************

TASK [IOS >> Get running config] **********************************************
ok: [csr1]

TASK [ASSERT >> Ensure CLI_OUTPUT is defined] *********************************
ok: [csr1] => {
    "changed": false
}

MSG:

All assertions passed

TASK [SETFACT >> Get current RT import/export list] ***************************
ok: [csr1]

TASK [SETFACT >> Determine RT import/export differences] **********************
ok: [csr1]

TASK [IOS >> Apply VPN config] ************************************************
changed: [csr1]

TASK [SETFACT >> Initialize empty FIB command list] ***************************
ok: [csr1]

TASK [SETFACT >> Build FIB command list based on intended VRFs] ***************
ok: [csr1] => (item=VRF VRF1)
ok: [csr1] => (item=VRF VRF2)
ok: [csr1] => (item=VRF VRF3)

TASK [ASSERT >> Ensure FIB_CMD_LIST and vrfs are same length] *****************
ok: [csr1] => {
    "changed": false
}

MSG:

All assertions passed

RUNNING HANDLER [DEBUG >> Print changes] **************************************
ok: [csr1] => {}

MSG:

[
    "vrf definition VRF1",
    "no route-target export 1:1",
    "vrf definition VRF2",
    "route-target import 65000:1",
    "vrf definition VRF3",
    "route-target import 65000:2",
    "no route-target export 1:1"
]


RUNNING HANDLER [PAUSE >> Wait for VPN route convergence] *********************
Pausing for 60 seconds
(ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
ok: [csr1]

TASK [IOS >> Capture FIB for all VRFs] ****************************************
ok: [csr1]

TASK [ASSERT >> Ensure VRF_FIB is defined] ************************************
ok: [csr1] => {
    "changed": false
}

MSG:

All assertions passed

TASK [INCLUDE >> Perform route and ping checks] *******************************
skipping: [csr1] => (item=VRF VRF2)
included: /home/ec2-user/vpnm/tasks/route_ping.yml for csr1
included: /home/ec2-user/vpnm/tasks/route_ping.yml for csr1

TASK [ASSERT >> Ensure route checks succeed] **********************************
ok: [csr1] => (item=does VRF VRF1 have route 10.3.3.0/30?) => {
    "changed": false,
    "route": "10.3.3.0/30"
}

MSG:

All assertions passed

ok: [csr1] => (item=does VRF VRF1 have route 10.4.4.0/24?) => {
    "changed": false,
    "route": "10.4.4.0/24"
}

MSG:

All assertions passed


TASK [IOS >> Ensure ping checks succeed] **************************************
ok: [csr1] => (item=can VRF VRF1 ping 10.3.3.1?)
ok: [csr1] => (item=can VRF VRF1 ping 10.4.4.44?)

TASK [ASSERT >> Ensure route checks succeed] **********************************
ok: [csr1] => (item=does VRF VRF3 have route 10.1.1.0/30?) => {
    "changed": false,
    "route": "10.1.1.0/30"
}

MSG:

All assertions passed

ok: [csr1] => (item=does VRF VRF3 have route 10.2.2.0/30?) => {
    "changed": false,
    "route": "10.2.2.0/30"
}

MSG:

All assertions passed


TASK [IOS >> Ensure ping checks succeed] **************************************
ok: [csr1] => (item=can VRF VRF3 ping 10.1.1.1?)
ok: [csr1] => (item=can VRF VRF3 ping 10.2.2.1?)

PLAY RECAP ********************************************************************
csr1                       : ok=15   changed=1    unreachable=0    failed=0
```
