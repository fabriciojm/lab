When we type `docker run` it launches a container that is able to do networking, i.e. communicate with other containers, or even the internet.

By using Linux features like (Network) [[Namespaces]], [[Cgroups]], [[Virtual Ethernet Pairs]] and [[Linux Network Bridges]], Docker is able to automatically set up the networking of containers.

- When we spin up a container with Docker, a bridge is automatically created, called `docker0` by default.
- Each bridge has a [[Virtual Ethernet Pairs]] (virtual cabling between bridge and container):
	- One inside the container (called `eth0` by default)
	- One attached to the bridge (called `veth-<unique-random-sequence>`)
- The bridge is in charge of forwarding packets to containers.

For a container to access the internet:
- The host that runs the containers needs to have ip forwarding allowed.
- [[Network Address Translation - NAT]], [[NAT Connection Tracking]]

Spin up two detached alpine containers, make them live for an hour. 
```bash
docker run -d --name c1 alpine sleep 3600
docker run -d --name c2 alpine sleep 3600
```

Check the bridge `docker0`
```bash
ip link show docker0
ip link show master docker0 # show enslaved interfaces to the master docker0 bridge interface
```

The first shows:
```
282: veth147e175@if281: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 36:f6:a5:15:75:3b brd ff:ff:ff:ff:ff:ff link-netnsid 0
284: veth73ba5b0@if283: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether aa:2b:2b:c2:a7:c2 brd ff:ff:ff:ff:ff:ff link-netnsid 1
```

See from inside a container
```bash
docker exec c1 ipaddr
```

Shows:
```
# Loobpack stuff, then:
281: eth0@if282: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```

In the example above, we can match the pair between virtual interfaces: 
- Host side: `282: veth147e175@if281`
- Container side:  `281: eth0@if282`

We can see the routing inside the container:
```bash
docker exec c1 ip route
```

From Docker commands
```bash
docker network inspect bridge
```

This shows a JSON output, look for IPAM (IP Address Manager) that contains the subnet and gateway definitions.
Also shows containers namespaces with their respective names and their respective IPs

Continues in [Container Networking by Hand](Container Networking by Hand.md)
