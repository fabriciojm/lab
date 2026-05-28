See [[Container Networking Basics]]

We are trying to do container networking by hand. A minimal network looks like this: two containers running in a host (called red and blue), that want to communicate between themselves and with the internet. 

![[Container Networking by Hand Drawing]]

By hand here means defining bridges, namespaces, veth pairs, etc.; i.e. everything in the diagram.

First instantiate net namespaces
```bash
sudo ip netns add blue
sudo ip netns add red
sudo ip netns exec red ip link show
```
Red links shoud show only loopback

Then add a link of type bridge and name `br-study`, wake it up, assign an ip address pointing to the bridge.
```bash
sudo ip link add br-study type bridge
sudo ip link set br-study up
sudo ip addr add 10.0.0.254/24 dev br-study
```

For the red container/namespace:
- Add the veth interface `veth-r` (that will live in the red namespace) with its peer veth in the bridge `veth-r-br`.
- Assign the veth `veth-r` to the red namespace
- Declare the veth `veth-r-br` as belonging (enslaved) to the bridge `br-study`
- Wake up veth `veth-r`

```bash
sudo ip link add veth-r type veth peer name veth-r-br
sudo ip link set veth-r netns red
sudo ip link set veth-r-br master br-study
sudo ip link set veth-r-br up
```

Inside the namespaces, we need to assign ips and up the interfaces (including loopback)

```bash
sudo ip netns exec red ip addr add 10.0.0.1/24 dev veth-r
sudo ip netns exec red ip link set veth-r up
sudo ip netns exec red ip link set lo up
```

Same for blue
```bash
sudo ip link add veth-b type veth peer name veth-b-br
sudo ip link set veth-b netns blue
sudo ip link set veth-b-br master br-study
sudo ip link set veth-b-br up
sudo ip netns exec blue ip addr add 10.0.0.2/24 dev veth-b
sudo ip netns exec blue ip link set veth-b up
sudo ip netns exec blue ip link set lo up
```

Can now test the network:
```bash
sudo ip netns exec red ping -c 3 10.0.0.2
```

But the namespaces cannot reach the internet yet, they don't have a default gateway configured.
```bash
sudo ip netns exec blue ip route
# 10.0.0.0/24 dev veth-b proto kernel scope link src 10.0.0.2
```

The default route for the machine is:
```bash
ip route show default
# default via 192.168.1.1 dev enp0s25 proto dhcp src 192.168.1.101 metric 100
```

Set it as the bridge for blue and red:
```bash
sudo ip netns exec blue ip route add default via 10.0.0.254
sudo ip netns exec red ip route add default via 10.0.0.254
```

Allow forwarding in the Linux kernel by setting the corresponding parameter to true (i.e. Linux can act as a router):
```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Define iptables rules to accept forward requests (input and output) for `br-study`:
```bash
sudo iptables -A FORWARD -i br-study -j ACCEPT
sudo iptables -A FORWARD -o br-study -j ACCEPT
```

Then a rule that defines the [[Network Address Translation - NAT]]/[[MASQUERADE NAT]]
```bash
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o enp0s25 -j MASQUERADE
```

Here
- `-t nat` type NAT
- `-A POSTROUTING` Append the rule after routing decisions.
- `-s 10.0.0.0/24` Source is network identifier with mask

And now the namespaces/containers can reach the internet. All this is running under the hood when one does `docker run`. Custom network topologies can be defined with [[Containers#Docker Compose]].

