#######
#
# Copyright (C) 2012 Phoenorama.org All Rights Reserved.
# Author: Philippe Blondin <pblondin@phoenorama.org>>
#
# This file is part of the Phoenorama program.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#
#######

'''
Created on Mar 27, 2012

@author: r00tmac
'''

from lxml import etree
from models import Report
                    
def parse(document):
    root = etree.parse(document)
    report = Report(root.xpath('/report/@id')[0])
    
    vulnerabilities = {}
    # iterate over vulnerabilities
    for result in root.xpath('//result'):
        host = result.xpath('host')[0].text
        if not vulnerabilities.has_key(host):
            vulnerabilities[host] = []
            
        vuln = {}
        
        # Summary
        vuln['description'] = result.xpath('description')[0].text.strip()
        vuln['name'] = result.xpath('nvt/name')[0].text
        vuln['service'] = result.xpath('port')[0].text
        
        # Risk
        vuln['risk_factor'] = result.xpath('nvt/risk_factor')[0].text
        vuln['cvss'] = result.xpath('nvt/cvss_base')[0].text
        vuln['threat'] = result.xpath('threat')[0].text
        
        # References
        vuln['nvtid'] = result.xpath('nvt/@oid')[0] #oid attribute
        cve = result.xpath('nvt/cve')[0].text
        vuln['cve'] = cve if cve != 'NOCVE' else None
        bid = result.xpath('nvt/bid')[0].text
        vuln['bid'] = bid if bid != 'NOBID' else None
        
        # add vuln to vulnerabilities dictionary
        vulnerabilities[host].append(vuln)
      
    openPorts = {}
    # iterate over open ports
    for port in root.xpath('//ports/port'):
        host = port.xpath('host')[0].text
        if not openPorts.has_key(host):
            openPorts[host] = []
        
        # add port to open ports dictionary
        openPorts[host].append(port.text)
        
    report.open_ports_by_host = openPorts
    report.vulnerabilities_by_host = __cleanupVulnerabilities(vulnerabilities)
    return report

def __cleanupVulnerabilities(vulnerabilities):
    # get rid of general information and open ports (duplicate information)
    filterOIDs = ['1.3.6.1.4.1.25623.1.0.900239',  # open tcp ports
                 '1.3.6.1.4.1.25623.1.0.103978',   # open upd ports
                 '1.3.6.1.4.1.25623.1.0.51662',    # traceroute
                 '1.3.6.1.4.1.25623.1.0.90022',    # ssh autorization
                 '1.3.6.1.4.1.25623.1.0.90011',    # smbclient not available
                 '1.3.6.1.4.1.25623.1.0.66286',    # unknown service
                 '1.3.6.1.4.1.25623.1.0.810003',   # host summary
                 '1.3.6.1.4.1.25623.1.0.19506',    # scan information
                 '1.3.6.1.4.1.25623.1.0.103079'    # DIRB (NASL wrapper)
                 '1.3.6.1.4.1.25623.1.0.110001',   # arachni (NASL wrapper)
                 '1.3.6.1.4.1.25623.1.0.14260',    # nikto (NASL wrapper)
                 '1.3.6.1.4.1.25623.1.0.80110'     # wapiti (NASL wrapper)
                 ]
    isNotGeneralInfo = lambda vuln: vuln['nvtid'] not in filterOIDs and True or False
    isNotOpenPort = lambda vuln: vuln['description'] != 'Open port.' and True or False
    for k in vulnerabilities:
        vulnerabilities[k] = filter(isNotGeneralInfo, vulnerabilities[k])
        vulnerabilities[k] = filter(isNotOpenPort, vulnerabilities[k])
    return vulnerabilities

if __name__ == '__main__':
    openvas_xml_report = file('../../docs/report-samples/openvas-2hosts-2012_03_24.xml', 'r')
    report = parse(openvas_xml_report)
    print report.printFullReport()
              
            