# Check_MK plugin to monitor Oxidized

This uses the [piggyback mechanism] to report the backup status of your network
devices to Check_MK. This means that:

* When a device is down, its failed backup check will not bother you.
* When Oxdizied has a problem, the backup checks of the devices will not bother
  you either. However, the Check_MK service might, because it's missing data!
* The hostnames in Check_MK have to case-sensitively match those in Oxidized. If
  they don't, you can use the "Hostname translation for piggybacked hosts"
  ruleset.

[piggyback mechanism]: https://docs.checkmk.com/latest/en/piggyback.html
