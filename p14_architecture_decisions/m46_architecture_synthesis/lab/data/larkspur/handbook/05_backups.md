# Backups and snapshots

Business and Enterprise plans take a backup of every server once a day. Business keeps each daily backup for 7 days and Enterprise keeps it for 30 days.

Starter plans have no automatic backups. Starter accounts can take manual snapshots from the console, up to 5 per server, and keep them until they delete them.

Backups and snapshots are stored in the same region as the server. Enterprise accounts can also keep a copy of each daily backup in a second region of their choice.

To restore, open the server in the console, choose Backups, and pick a backup or snapshot. Restoring replaces the server disk with the backup, so anything written after the backup was taken is lost. Take a snapshot first if you may need the current state.

Backups are deleted together with the server. A server deleted by mistake cannot be recovered from its own backups.
