#!/usr/bin/env python

import cobra
import re
import urllib3
import sys

from cobra.mit.session import LoginSession
from cobra.mit.access import MoDirectory
from cobra.mit.request import DnQuery

urllib3.disable_warnings() #Disable HTTPS warnings

apic_url = ''
apic_user = ''
apic_password = ''

loginSession = LoginSession(apic_url, apic_user, apic_password) #Setup Login credentials
md = MoDirectory(loginSession)
md.login() #Login

dq1 = DnQuery('uni/infra')
dq1.queryTarget='subtree'
dq1.classFilter='infraAccPortP'
InterfaceProfiles = md.query(dq1)

for IF in InterfaceProfiles:

    dq2 = DnQuery('uni/infra/accportprof-'+IF.name+'/hports-'+IF.name+'-IF-typ-range/portblk-block2')
    dq2.queryTarget='subtree'
    dq2.classFilter='infraPortBlk'
    AccPorts= md.query(dq2)
    if len(AccPorts)!=0:
        print IF.name + ' = ' + AccPorts[0].fromCard + '/' + AccPorts[0].fromPort

raw_input('Press Enter to continue...')
