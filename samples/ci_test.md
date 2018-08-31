Expected output from running CI tests using `make test`. It should
be a very fast test with no failures.

```
$ time make test
Starting  lint
find . -name "*.yml" | xargs yamllint -s
find . -name "*.py" | xargs pylint
Using config file /home/ec2-user/vpnm/.pylintrc

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

find . -name "*.py" | xargs bandit
[main] INFO profile include tests: None
[main] INFO profile exclude tests: None
[main] INFO cli include tests: None
[main] INFO cli exclude tests: None
[main] INFO running on Python 2.7.5
Run started:2018-08-31 20:47:34.077783

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 74
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
Completed lint
Starting  unit tests
ansible-playbook tests/unittest_playbook.yml

PLAY [Perform automated filter (unit) testing] *********************************

TASK [SYS >> Store task file search string] ************************************
ok: [localhost]

TASK [SYS >> Get files matching 'test_*[.]yml'] ********************************
ok: [localhost]

TASK [SYS >> Assemble file paths into single list] *****************************
ok: [localhost]

TASK [DEBUG >> Print file paths] ***********************************************
ok: [localhost] => {
    "FILE_LIST": [
        "/home/ec2-user/vpnm/tests/tasks/test_ios_vrf_rt.yml", 
        "/home/ec2-user/vpnm/tests/tasks/test_rt_diff.yml"
    ]
}

TASK [include_tasks] ***********************************************************
included: /home/ec2-user/vpnm/tests/tasks/test_ios_vrf_rt.yml for localhost
included: /home/ec2-user/vpnm/tests/tasks/test_rt_diff.yml for localhost

TASK [Store IOS VRF text] ******************************************************
ok: [localhost]

TASK [Perform parsing] *********************************************************
ok: [localhost]

TASK [Print structured data] ***************************************************
ok: [localhost] => {
    "data": {
        "1": {
            "route_export": [
                "65000:111"
            ], 
            "route_import": [
                "65000:101"
            ]
        }, 
        "2": {
            "route_export": [
                "65000:111", 
                "65000:222"
            ], 
            "route_import": [
                "65000:101", 
                "65000:202"
            ]
        }, 
        "3": {
            "route_export": [], 
            "route_import": [
                "65000:303"
            ]
        }
    }
}

TASK [ASSERT >> Ensure VRF 1 parsing succeeded] ********************************
ok: [localhost] => {
    "changed": false
}

MSG:

All assertions passed


TASK [ASSERT >> Ensure VRF 2 parsing succeeded] ********************************
ok: [localhost] => {
    "changed": false
}

MSG:

All assertions passed


TASK [ASSERT >> Ensure VRF 3 parsing succeeded] ********************************
ok: [localhost] => {
    "changed": false
}

MSG:

All assertions passed


TASK [Store IOS VRF text] ******************************************************
ok: [localhost]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "run_vrf_dict": {
        "1": {
            "route_export": [], 
            "route_import": [
                "65000:1"
            ]
        }, 
        "2": {
            "route_export": [
                "65000:2"
            ], 
            "route_import": [
                "65000:222", 
                "65000:1"
            ]
        }, 
        "3": {
            "route_export": [], 
            "route_import": [
                "65000:2", 
                "65000:333"
            ]
        }
    }
}

TASK [Find RT differences] *****************************************************
ok: [localhost]

TASK [Print structured data] ***************************************************
ok: [localhost] => {
    "rt_updates": [
        {
            "add_rte": [
                "65000:2"
            ], 
            "add_rti": [], 
            "del_rte": [], 
            "del_rti": [], 
            "description": "first VRF", 
            "name": "1", 
            "rd": "65000:1"
        }, 
        {
            "add_rte": [], 
            "add_rti": [], 
            "del_rte": [], 
            "del_rti": [
                "65000:222"
            ], 
            "description": "second VRF", 
            "name": "2", 
            "rd": "65000:2"
        }, 
        {
            "add_rte": [
                "65000:1"
            ], 
            "add_rti": [], 
            "del_rte": [], 
            "del_rti": [
                "65000:333"
            ], 
            "description": "third VRF", 
            "name": "3", 
            "rd": "65000:3"
        }
    ]
}

TASK [ASSERT >> Ensure VRF 1 RT difference succeeded] **************************
ok: [localhost] => {
    "changed": false
}

MSG:

All assertions passed


TASK [ASSERT >> Ensure VRF 2 RT difference succeeded] **************************
ok: [localhost] => {
    "changed": false
}

MSG:

All assertions passed


TASK [ASSERT >> Ensure VRF 3 RT difference succeeded] **************************
ok: [localhost] => {
    "changed": false
}

MSG:

All assertions passed


PLAY RECAP *********************************************************************
localhost                  : ok=19   changed=0    unreachable=0    failed=0   

Completed unit tests
Starting  playbook tests
ansible-playbook tests/test_playbook.yml --skip-tags "do_ssh"

PLAY [Manage MPLS L3VPN route-targets] *****************************************

TASK [ASSERT >> Ensure CLI_OUTPUT is defined] **********************************
ok: [csr1] => {
    "changed": false
}

MSG:

All assertions passed


TASK [SETFACT >> Get current RT import/export list] ****************************
ok: [csr1]

TASK [SETFACT >> Determine RT import/export differences] ***********************
ok: [csr1]

TASK [SETFACT >> Initialize empty FIB command list] ****************************
ok: [csr1]

TASK [SETFACT >> Build FIB command list based on intended VRFs] ****************
ok: [csr1] => (item=VRF 1)
ok: [csr1] => (item=VRF 2)
ok: [csr1] => (item=VRF 3)

TASK [ASSERT >> Ensure FIB_CMD_LIST and vrfs are same length] ******************
ok: [csr1] => {
    "changed": false
}

MSG:

All assertions passed


TASK [ASSERT >> Ensure VRF_FIB is defined] *************************************
ok: [csr1] => {
    "changed": false
}

MSG:

All assertions passed


TASK [INCLUDE >> Perform route and ping checks] ********************************
skipping: [csr1] => (item=VRF 2) 
included: /home/ec2-user/vpnm/tasks/route_ping.yml for csr1
included: /home/ec2-user/vpnm/tasks/route_ping.yml for csr1

TASK [ASSERT >> Ensure route checks succeed] ***********************************
ok: [csr1] => (item=does VRF 1 have route 10.3.3.0/30?) => {
    "changed": false, 
    "route": "10.3.3.0/30"
}

MSG:

All assertions passed

ok: [csr1] => (item=does VRF 1 have route 10.4.4.0/24?) => {
    "changed": false, 
    "route": "10.4.4.0/24"
}

MSG:

All assertions passed


TASK [ASSERT >> Ensure route checks succeed] ***********************************
ok: [csr1] => (item=does VRF 3 have route 10.1.1.0/30?) => {
    "changed": false, 
    "route": "10.1.1.0/30"
}

MSG:

All assertions passed

ok: [csr1] => (item=does VRF 3 have route 10.2.2.0/30?) => {
    "changed": false, 
    "route": "10.2.2.0/30"
}

MSG:

All assertions passed


PLAY RECAP *********************************************************************
csr1                       : ok=11   changed=0    unreachable=0    failed=0   

Completed playbook tests

real    0m5.432s
user    0m4.870s
sys     0m0.555s
```
