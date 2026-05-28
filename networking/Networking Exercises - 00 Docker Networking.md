See [[Container Networking by Hand]]

Following https://github.com/drewelliott/kubecraft/blob/main/lessons/clab/00-docker-networking/exercises/README.md

# Inspect Docker's Network Plumbing

- Create docker containers c1 and c2, let them hold for an hour
- Show the `docker0` bridge in the host
- Show the interfaces attached to `docker0`

```bash
docker run -d --name c1 alpine sleep 3600
docker run -d --name c2 alpine sleep 3600
ip link show docker0
ip link show master docker0
```

I got

- `295: veth5844196@if294: (...) link-netnsid 19`
- `297: vetha2f5023@if296: (...) link-netnsid 21`

Inspect container to verify
```bash
docker exec c1 ip addr
docker exec c1 ip route
```

Docker's view:
```bash
docker network inspect bridge
```


# Container Network from Scratch

See again [[Container Networking by Hand]]

Answers to the final questions of the exercise:
- The ping to `127.0.0.1` failed before bringing up `lo` exactly because that IP address is reserved for the own host. If loopback is not up (it's down by default in new namespaces), the host cannot communicate with itself via network. The loopback interface is not that different from bridge-connected interfaces, as it needs to be up to communicate.
- The command `ip link show master br-study` shows which interfaces are attached to the bridge `br-study`. In our case that is two:
	- `304: veth-r-br@if305: (...) link-netns red`
	- `306: veth-b-br@if307: (...) link-netns blue`
  we have the two veths we set up, on the host side: 304 is pointing to interface 305 in the red namespace and 306 is pointing to interface 307 in the blue namespace.
- The setups are conceptually the same as Docker. In practice, Docker needs to automate all this, and many names get a random unique string identifier (?)

# Enable NAT

Also done in [[Container Networking by Hand]]

List POSTROUTING rules (verbose):
```bash
sudo iptables -t nat -L POSTROUTING -v
```

Answers:
- Masquerade rule is a dynamic source [[Network Address Translation - NAT]], i.e. it rewrites packet SRC as that of the host (external). The NAT itself keeps a conection tracking
- We need IP forwarding enabled so that the kernel can work as a router (by default, for security reasons, it can't).
- A security feature of Docker is to set the FORWARD chain policy to DROP, allowing only forwarding in its internal network (e.g. the default `docker0`)
- Docker allows another address in the network (that of the docker engine/hypervisor/vm?) that is 172.17.0.0/16

Take a look at https://github.com/drewelliott/kubecraft/tree/main/lessons/clab/00-docker-networking/solutions#answers-to-questions-1

```shell
$ sudo iptables -L FORWARD -v
Chain FORWARD (policy DROP 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
(...)
    0     0 DOCKER-USER  all  --  any    any     anywhere             anywhere
    0     0 DOCKER-FORWARD  all  --  any    any     anywhere             anywhere
# We added by hand, explicitly:
    0     0 ACCEPT     all  --  br-study any     anywhere             anywhere
    0     0 ACCEPT     all  --  any    br-study  anywhere             anywhere

(...)
```

# Break/Fix -- Bridge Down

Run
```bash
sudo ip link set br-study down
```

Then `sudo ip netns exec red ping -c 2 10.0.0.2` doesn't work

Answers
- Run `ip link show br-study` State `DOWN` means that the entity is not communicating anything, it's turned off.
- Run `ip link show master br-study`. It shows the veth pairs up. The analogous example would be to have something plugged into a network bridge/switch but the device itself has no power or is off.

```bash
sudo ip link set br-study up
```

Then ping works again.

# Break/Fix -- Missing Masquerade

Run

```bash
sudo iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o enp0s25 -j MASQUERADE
```

(`-D`: delete)

Answers:
- Local connectivity still works:
```bash
sudo ip netns exec red ping -c 3 10.0.0.2
sudo ip netns exec blue ping -c 3 10.0.0.1
```
- NAT table `sudo iptables -t nat -L POSTROUTING -v -n` gives the nat policies, but there's no nat rule for the `br-study`.
- `$ sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o enp0s25 -j MASQUERADE` makes it work 







