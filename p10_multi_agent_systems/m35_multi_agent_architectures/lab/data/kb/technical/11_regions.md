# Regions

Larkspur Cloud runs five regions: Frankfurt and Dublin in the EU, Virginia and Oregon in the United States, and Singapore.

Every plan can use every region. Data stays in the region where it was created unless you copy it elsewhere, so customers with EU data residency requirements should create their servers in Frankfurt or Dublin.

A server cannot be moved between regions in place. To move one, take a snapshot, copy it to the new region from the console, and create a server from the copy. The new server gets a new IP address.

Outbound traffic between two Larkspur regions counts towards the traffic allowance like any other outbound traffic.
