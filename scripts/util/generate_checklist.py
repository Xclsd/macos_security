#!/usr/bin/env python3

from pathlib import Path
import plistlib
import argparse
from collections import OrderedDict
import re
import os
import platform


def do_regex(stig_id, stig_title, result, stig, exempt, exempt_reason, ruleid):
    checklist_xml = '''
    <VULN>'''
    regex = r"<Group id=\"(V-..*\d)\">.*.{}".format(stig_id)
    #Vulnerability ID        
    matches = re.search(regex,stig)
    if matches:
        
        checklist_xml = checklist_xml + '''
        <STIG_DATA>
            <VULN_ATTRIBUTE>Vuln_Num</VULN_ATTRIBUTE>
            <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(matches.group(1))
            
    regex = r"severity=\"(.*\S)\">.*.{}".format(stig_id)
    #severity
    matches = re.search(regex,stig)
    if matches:
        
        checklist_xml = checklist_xml + '''
        <STIG_DATA>
            <VULN_ATTRIBUTE>Severity</VULN_ATTRIBUTE>
            <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(matches.group(1))

    regex = r"<title>(SRG.*\d)<\/title>.*.{}".format(stig_id)
    matches = re.search(regex,stig)
    #SRG
    if matches:
        
        checklist_xml = checklist_xml + '''
        <STIG_DATA>
            <VULN_ATTRIBUTE>Group_Title</VULN_ATTRIBUTE>
            <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(matches.group(1))


    regex = r"Rule id=\"(.*\S)\" we.*.{}".format(stig_id)
    matches = re.search(regex,stig)
    #RuleID
    if matches:
        
        checklist_xml = checklist_xml + '''
        <STIG_DATA>
            <VULN_ATTRIBUTE>Rule_ID</VULN_ATTRIBUTE>
            <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(matches.group(1))

    
    checklist_xml = checklist_xml + '''
        <STIG_DATA>
            <VULN_ATTRIBUTE>Rule_Ver</VULN_ATTRIBUTE>
            <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(stig_id)
    

    regex = r"{}.*<title>(.*.)<\/title>".format(stig_id)
    #Title
    matches = re.search(regex,stig)
    if matches:
        
        checklist_xml = checklist_xml + '''
        <STIG_DATA>
                <VULN_ATTRIBUTE>Rule_Title</VULN_ATTRIBUTE>
                <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(matches.group(1))
    
    regex = r"{}.*.<description>&lt;VulnDiscussion&gt;((\n|.)*?)&lt;\/VulnDiscussion&gt".format(stig_id)
    #Vul Discussion
    matches = re.search(regex,stig)
    if matches:
        
        checklist_xml = checklist_xml + '''
        <STIG_DATA>
                <VULN_ATTRIBUTE>Vuln_Discuss</VULN_ATTRIBUTE>
                <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(matches.group(1))

    checklist_xml = checklist_xml + '''
    <STIG_DATA>
        <VULN_ATTRIBUTE>IA_Controls</VULN_ATTRIBUTE>
        <ATTRIBUTE_DATA></ATTRIBUTE_DATA>
    </STIG_DATA>'''
    
    regex = r"{}.(\n|.)*?.<check-content>((\n|.)*?)<\/check-content>".format(stig_id)
    matches = re.search(regex, stig)
    if matches:
        #Check Content
        
        checklist_xml = checklist_xml + '''
    <STIG_DATA>
        <VULN_ATTRIBUTE>Check_Content</VULN_ATTRIBUTE>
        <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
    </STIG_DATA>'''.format(matches.group(2))
    regex = r"<version>{}<\/version>(?:.|\n)*?<fixtext fixref=\".*?\">([^<]+)<\/fixtext>".format(stig_id)
    #fix_text
    matches = re.search(regex,stig)
    if matches:
        checklist_xml = checklist_xml + '''
    <STIG_DATA>
        <VULN_ATTRIBUTE>Fix_Text</VULN_ATTRIBUTE>
        <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
    </STIG_DATA>'''.format(matches.group(1))

    regex = r"weight=\"(.*\d)\".*.{}".format(stig_id)
    #weight
    matches = re.search(regex,stig)
    if matches:
        
        checklist_xml = checklist_xml + '''
        <STIG_DATA>
					<VULN_ATTRIBUTE>False_Positives</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>False_Negatives</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Documentable</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>false</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Mitigations</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Potential_Impact</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Third_Party_Tools</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Mitigation_Control</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Responsibility</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Security_Override_Guidance</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Check_Content_Ref</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>M</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Weight</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>{weight}</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Class</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>Unclass</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>STIGRef</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>{title}</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>TargetKey</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>5543</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>STIG_UUID</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>bc527f01-5874-4b6a-adae-50e51af1e867</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>LEGACY_ID</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>LEGACY_ID</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>'''.format(weight = matches.group(1), title = stig_title)
    
    regex = r"{}(\n|.)*?(<ident system=\".*.\">CCI-.*\d)<\/ident>".format(stig_id)
    matches = re.finditer(regex, stig, re.MULTILINE)
    comment = str()
    for matchNum, match in enumerate(matches, start=1):
        
        for groupNum in range(1, 2):
            #CCI
            groupNum = groupNum + 1
            cci_group = "{group}".format(group = match.group(groupNum))
            pattern = r'CCI-(\d+)'
            matches = re.findall(pattern, cci_group)
            cci_numbers = ['CCI-' + match for match in matches]
            
            for cci in cci_numbers:
                checklist_xml = checklist_xml + '''
        <STIG_DATA>
            <VULN_ATTRIBUTE>CCI_REF</VULN_ATTRIBUTE>
            <ATTRIBUTE_DATA>{}</ATTRIBUTE_DATA>
        </STIG_DATA>'''.format(cci)
        
        if exempt:
            exempt_reason = "Exemption Reason: {}".format(exempt_reason)
        if ruleid != "":
            comment = "Checked with mscp compliance script - {}".format(ruleid)
    checklist_xml = checklist_xml + '''
        <STATUS>{}</STATUS>
        <FINDING_DETAILS>{}</FINDING_DETAILS>
        <COMMENTS>{}</COMMENTS>
        <SEVERITY_OVERRIDE></SEVERITY_OVERRIDE>
        <SEVERITY_JUSTIFICATION></SEVERITY_JUSTIFICATION>
    </VULN>'''.format(result, exempt_reason, comment)	
    return checklist_xml			

def validate_file(arg):
    if (file := Path(arg)).is_file():
        return file
    else:
        raise FileNotFoundError(arg)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plist', '-p', type=validate_file, help="Input plist scan", required=True)
    parser.add_argument('--disastig','-d',type=validate_file, help="DISA STIG File", required=True)
    args = parser.parse_args()

    with open(args.plist, 'rb') as fp:
        pl = plistlib.load(fp)
    
    managedDict = []
    
    managedPref = "/Library/Managed Preferences/" + str(args.plist).split("/")[-1]
    if os.path.exists(managedPref):
        with open(managedPref, 'rb') as mPl:
            managedDict = plistlib.load(mPl)
    
    file = open(args.disastig, "r")
    stig = file.read()
    sortedpl = OrderedDict(sorted(pl.items()))
    data = []
    result_stig_id_set = set()
    disa_stig_id_set = set()
    for rule,sub in sortedpl.items():
        results_array = {}
        if rule == "lastComplianceCheck":
            continue
        try:
            results_array = {"id": rule,
            "finding": sub['finding'],
            "reference": sub['reference']}
            result_stig_id_set.add(sub['reference'])
        except:
            results_array = {"id": rule,
            "finding": sub['finding'],
            "reference": "N/A"}
        try:
            if rule in managedDict:
                results_array['exemption'] = managedDict[rule]['exempt']
                results_array['exemption_reason'] = managedDict[rule]['exempt_reason']
            else:
                results_array['exemption'] = sub['exempt']
                results_array['exemption_reason'] = sub['exempt_reason']

        
        except:
            results_array['exemption'] = False
            results_array['exemption_reason'] = ""
            
        data.append(results_array)
    regex = r"<title>(.*?.)<\/title><description>"
    
    matches = re.search(regex, stig)
    stigtitle = str()
    #stig title
    if matches:
        
        stigtitle = matches.group(1)

    regex = r"id=\"(.*)\" xml:lang=\"en\" xmlns="
    #stig title id
    matches = re.search(regex,stig)
    stig_title_id = str()

    if matches:
        stig_title_id = matches.group(1)

    regex = r"<plain-text id=\"release-info\">(.*)<plain-text"
    matches = re.search(regex, stig)
    #release info
    release_info = str()
    if matches:
        release_info = matches.group(1).split("<")[0]

    big_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<!--DISA STIG Viewer :: 2.12-->
<CHECKLIST>
	<ASSET>
		<ROLE>None</ROLE>
		<ASSET_TYPE>Computing</ASSET_TYPE>
		<HOST_NAME>{hostname}</HOST_NAME>
		<HOST_IP></HOST_IP>
		<HOST_MAC></HOST_MAC>
		<HOST_FQDN></HOST_FQDN>
		<TARGET_COMMENT></TARGET_COMMENT>
		<TECH_AREA></TECH_AREA>
		<TARGET_KEY>5543</TARGET_KEY>
		<WEB_OR_DATABASE>false</WEB_OR_DATABASE>
		<WEB_DB_SITE></WEB_DB_SITE>
		<WEB_DB_INSTANCE></WEB_DB_INSTANCE>
	</ASSET>
	<STIGS>
		<iSTIG>
			<STIG_INFO>
				<SI_DATA>
					<SID_NAME>version</SID_NAME>
					<SID_DATA>1</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>classification</SID_NAME>
					<SID_DATA>UNCLASSIFIED</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>customname</SID_NAME>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>stigid</SID_NAME>
					<SID_DATA>{stigid}</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>description</SID_NAME>
					<SID_DATA>This Security Technical Implementation Guide is published as a tool to improve the security of Department of Defense (DOD) information systems. The requirements are derived from the National Institute of Standards and Technology (NIST) 800-53 and related documents. Comments or proposed revisions to this document should be sent via email to the following address: disa.stig_spt@mail.mil.</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>filename</SID_NAME>
					<SID_DATA>{filename}</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>releaseinfo</SID_NAME>
					<SID_DATA>{releaseinfo}</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>title</SID_NAME>
					<SID_DATA>{title}</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>uuid</SID_NAME>
					<SID_DATA>1cf39da6-778a-45de-a48e-9e999f5580b2</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>notice</SID_NAME>
					<SID_DATA>terms-of-use</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>source</SID_NAME>
				</SI_DATA>
			</STIG_INFO>'''.format(stigid = stig_title_id, filename = os.path.basename(args.disastig), releaseinfo = release_info, title = stigtitle, hostname = platform.node())
    for entry in data:
        
        if entry['reference'] == "N/A":
            continue
        if entry['finding'] == 0:
            big_xml = big_xml + do_regex(entry['reference'], stigtitle + " " + release_info, "NotAFinding", stig, entry['exemption'], entry['exemption_reason'], entry['id'])
        if entry['finding'] == 1:
            big_xml = big_xml + do_regex(entry['reference'], stigtitle + " " + release_info, "Open", stig, entry['exemption'], entry['exemption_reason'], entry['id'])

    regex = r"(APPL-.\d-*\d.\d.\d.)"
    disa_stig_id_set = set(re.findall(regex, stig))
    missing = list(sorted(disa_stig_id_set - result_stig_id_set))

    for id in missing:
        big_xml = big_xml + do_regex(id, stigtitle + " " + release_info, "Not_Reviewed", stig, False, "", "")

    big_xml = big_xml + '''
    </iSTIG>
	</STIGS>
</CHECKLIST>'''
    print(big_xml)
if __name__ == "__main__":
    main()