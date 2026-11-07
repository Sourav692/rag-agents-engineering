# Outages and status

The status page at status.larkspur.example shows the health of every region and every service: servers, block storage, object storage, databases and the API. Probes check each region once a minute, and the status page records every incident with its start and end time.

During an incident, follow the status page for updates. Engineers publish a root-cause report within 72 hours of recovery.

You can subscribe to status updates by email or webhook from the status page. Subscriptions can be limited to the regions you use.

Planned maintenance is announced on the status page at least 7 days ahead. Most maintenance needs no action; when a server has to restart, the notice says when.

If a single server stops responding while the status page shows its region as healthy, the problem is usually inside the server. You can reboot a server from the console. A reboot takes about a minute and does not change the server IP address. If a reboot does not help, open a ticket in the Technical category.
