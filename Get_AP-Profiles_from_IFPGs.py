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
md.login()

dq1 = DnQuery('uni/<INSERT TENANT NAME>/<<INSERT AP PROFILE NAME>') #Query the Tenant
dq1.queryTarget='children' #request all children from Tenant
Bridge_Domains = md.query(dq1) #Get list of Bridge Domains (VLANs)
IFPG_List=[]
temp='temp'
ifpg_check = re.compile("") #create regex for your own naming convention of IFPGs to filter children of AP profile

for bd in Bridge_Domains:
    dq2 = DnQuery('uni/<INSERT TENANT NAME>/<<INSERT AP PROFILE NAME>/epg-'+bd.name) #create query for each BD found with previous query
    dq2.queryTarget='children' #target children (static ports)
    dq2.subtreeClassFilter='fvRsPathAtt'
    StaticPorts = md.query(dq2) #Get Result
    for epg in StaticPorts:
        if re.findall(ifpg_check, str(epg.dn)): #Check if entry if InterFace Policy Group
            temp = re.findall(ifpg_check, str(epg.dn)) #Save IFPG if entry checks out
        if len(IFPG_List)==0:
            IFPG_List.append(temp)
        else:
            for i in xrange(len(IFPG_List)):
                if IFPG_List[i]!=temp:
                    tmp_bit=1
                else:
                    tmp_bit=0
                    break
            if tmp_bit==1:
                IFPG_List.append(temp)

temporary="temp"

for vm in IFPG_List:
    vl_list=[]
    for bd in Bridge_Domains:
        dq3 = DnQuery('uni/<INSERT TENANT NAME>/<<INSERT AP PROFILE NAME>/epg-'+bd.name) #create second query for each BD found with previous query
        dq3.queryTarget='children' #target children (static ports)
        dq3.subtreeClassFilter='fvRsPathAtt'
        StaticPorts2 = md.query(dq3)
        for associations in StaticPorts2:
            if re.findall(ifpg_check, str(associations.dn)): #Check if entry if InterFace Policy Group
                temporary = re.findall(ifpg_check, str(associations.dn)) #Save IFPG if entry checks out
            else: 
                temporary = 'null'
            if vm == temporary:
                vl_list.append(bd.name)
    if len(vl_list) !=0:
        print vm
        print vl_list
    
raw_input('Press Enter to continue...') 
