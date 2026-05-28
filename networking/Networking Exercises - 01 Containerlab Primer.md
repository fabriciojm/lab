# Deploy and Explore

```bash
clab deploy/inspect
```

```
docker exec -it clab-first-lab-srl1 sr_cli
```

Inside SR CLI:
```
show version
show interface
```

Output of inspect
```
$ containerlab inspect -t topology/lab.clab.yml
15:20:37 INFO Parsing & checking topology file=lab.clab.yml
╭─────────────────────┬───────────────────────────────┬─────────┬───────────────────╮
│         Name        │           Kind/Image          │  State  │   IPv4/6 Address  │
├─────────────────────┼───────────────────────────────┼─────────┼───────────────────┤
│ clab-first-lab-srl1 │ srl                           │ running │ 172.20.20.3       │
│                     │ ghcr.io/nokia/srlinux:24.10.1 │         │ 3fff:172:20:20::3 │
├─────────────────────┼───────────────────────────────┼─────────┼───────────────────┤
│ clab-first-lab-srl2 │ srl                           │ running │ 172.20.20.2       │
│                     │ ghcr.io/nokia/srlinux:24.10.1 │         │ 3fff:172:20:20::2 │
╰─────────────────────┴───────────────────────────────┴─────────┴───────────────────╯
```

Show version:

```
A:srl2# show version
------------------------------------------------------------------------------------------------------------------------------------------------
Hostname             : srl2
Chassis Type         : 7220 IXR-D2L
Part Number          : Sim Part No.
Serial Number        : Sim Serial No.
System HW MAC Address: 1A:CE:01:FF:00:00
OS                   : SR Linux
Software Version     : v24.10.1
Build Number         : 492-gf8858c5836
Architecture         : x86_64
Last Booted          : 2026-05-22T10:16:22.625Z
Total Memory         : 7632062 kB
Free Memory          : 1770847 kB
------------------------------------------------------------------------------------------------------------------------------------------------
```

Show interface brief:
```
A:srl2# show interface brief
+---------------------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+
|        Port         |      Admin State      |      Oper State       |         Speed         |         Type          |      Description      |
+=====================+=======================+=======================+=======================+=======================+=======================+
| ethernet-1/1        | enable                | up                    | 25G                   |                       |                       |
| ethernet-1/2        | disable               | down                  | 25G                   |                       |                       |
| ethernet-1/3        | disable               | down                  | 25G                   |                       |                       |
| ethernet-1/4        | disable               | down                  | 25G                   |                       |                       |
| ethernet-1/5        | disable               | down                  | 25G                   |                       |                       |
| ethernet-1/6        | disable               | down                  | 25G                   |                       |                       |
| ethernet-1/7        | disable               | down                  | 25G                   |                       |                       |
...
| mgmt0               | enable                | up                    | 1G                    |                       |                       |
+---------------------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+

```

I believe the first interface is up only because the topoly defines a single veth pair, so SRL enables a single interface for connection...

# Modify the Topology

```bash
containerlab destroy -t topology/lab.clab.yml
```

Add a third node and make a sequential connection:

```yaml
# Lesson 1: First Containerlab Topology
# Three SR Linux nodes connected directly

name: three-nodes-lab

topology:
  nodes:
    # First SR Linux node
    srl1:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

    # Second SR Linux node
    srl2:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

    # Third SR Linux node
    srl3:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

  links:
    # Connect srl1's ethernet-1/1 to srl2's ethernet-1/1
    - endpoints: ["srl1:e1-1", "srl2:e1-1"]
    # Connect srl2's ethernet-1/2 to srl3's ethernet-1/2
    - endpoints: ["srl2:e1-2", "srl3:e1-2"]
```

# Generate Documentation

```shell
containerlab graph -t exercises/three-node.clab.yml -o exercises/topology.png
```

The image served in the browser is this one. But the way it was displayed by default was really confusing (links overlapping).

![[Pasted image 20260522154937.png]]

It says to generate a graph (png) with this:

```shell
containerlab graph -t exercises/three-node.clab.yml -o exercises/topology.png
```

But in reality it should be

```bash
containerlab graph -t exercises/three-node.clab.yml --dot
```

This was actually broken and I contributed a few lines to containerlab! [PR 3202](https://github.com/srl-labs/containerlab/commit/05cac296b6a669cd56aab6b1950c1c54f9134742).

In any case, containerlab devs are really proud (as they should) of their VS Code extension that provides much more useful graphs.

https://containerlab.dev/manual/vsc-extension/

Inspect in json format

```bash
containerlab inspect -t exercises/three-node.clab.yml --format json > exercises/lab-info.json
```

# Find Resources

## Documentation

https://containerlab.dev/manual/kinds/srl/

Startup configurations can modify the default node configuration through the `startup-config` statement. The rendered config can be found at `/tmp/clab-default-config` and is saved in `clab-<lab_name>/<node-name>/config/config.json`.

Many changes are possible:
- enabling interfaces, enabling [[LLDP]]
- enabling [[gNMI]]/[[gNOI]]/[[JSON-RPC]] (API/protocols used to manage and monitor network services, built on [[RPC]]/encoding mechanisms)
- creating [[TLS]] server certificates
- setting `mgmt0 subinterface 0 ip-mtu` to the [[Maximum Transmission Unit - MTU]] value of the underlying container runtime network.

A checkpoint of the config is generated once the default and user-provided configs are applied, it's called `clab-initial`.

> [!info] From the solutions:
>
> Key configuration options:
>  - `startup-config`: Path to configuration file
>  - `license`: Path to license file (not needed for basic features)
>  - `type`: SR Linux variant (ixrd1, ixrd2, etc.)
>
>  **Example Community Labs:**
>  
>  - [https://github.com/srl-labs/srl-labs](https://github.com/srl-labs/srl-labs) - Nokia's official examples
>  - [https://github.com/srl-labs/containerlab/tree/main/lab-examples](https://github.com/srl-labs/containerlab/tree/main/lab-examples) - Built-in examples
>  - [https://clabs.netdevops.me/](https://clabs.netdevops.me/) - Community lab collection

The configuration can be provided in two ways.

### Full configuration in JSON format

SR Linux persists its configuration as a JSON file found in `/etc/opt/srlinux/config.json`. Can be used as a startup config

```yaml
name: srl_lab
topology:
  nodes:
    srl1:
      kind: nokia_srlinux
      type: ixr-d3
      image: ghcr.io/nokia/srlinux
      # a path to the full config in JSON format relative to the current working directory
      startup-config: myconfig.json
```
### Partial configuration through the SR Linux CLI

A typical screnario is that nodes boot with a default config. The modifications to the SR Linux configuration can be captured in the form of cli instructions using the `info` command, which can be saved into a file, then passed to the topology file as a startup configuration:

```yaml
name: srl_lab
topology:
  nodes:
    srl1:
      kind: nokia_srlinux
      type: ixr-d3
      image: ghcr.io/nokia/srlinux
      # a path to the partial config in CLI format relative to the current working directory
      startup-config: myconfig.cli
```

---
Licenses are provided with the `license` directive:

```yaml
name: mylab

topology:
  nodes:
    leaf1:
      kind: nokia_srlinux
      image: ghcr.io/nokia/srlinux:latest
      license: /absolute/path/to/license.key
    leaf2:
      kind: nokia_srlinux
      image: ghcr.io/nokia/srlinux:latest
      license: /absolute/path/to/license.key
```

## GitHub Repo

I found this repo:

https://github.com/holo-routing/containerlab-topologies/

It contains pre-configured network topologies that can be used for testing interoperability or labbing.

More specifically: https://github.com/holo-routing/containerlab-topologies/tree/master/mpls-ldp

Demonstrates [[Multiprotocol Label Switching - MPLS]] label-switched routing using [[Label Distribution Protocol - LDP]] over a [[Open Shortest Path First - OSPF]]. 

In order:
- [[Open Shortest Path First - OSPF]] decides the path.
- [[Label Distribution Protocol - LDP]] assigns labels for those paths.
- [[Multiprotocol Label Switching - MPLS]] forwards using labels instead of doing IP lookups each time.

Those mechanisms are prescribed in the directory. There, topology defines the wiring: nodes, images, interfaces, links (think about endpoints). In files like interfaces/rt1 the interfaces of the nodes are defined, gives IP connectivity. In files like holo/rt1.conf there are sections enabling OSPF, LDP and MPLS.

## Community

A user wanted to have a containerlab host (alpine) deployed with ssh access at startup.

Another user had a cool solution. His answer:

> I built a docker image called labhost-lite specifically for this purpose. It has common networking utilities and sets up an ssh server with a standard login and password. [https://github.com/CapnCheapo/labhost-lite](https://github.com/CapnCheapo/labhost-lite "https://github.com/CapnCheapo/labhost-lite") Can be pulled in a topology file with the following: 
> `image: ghcr.io/capncheapo/labhost-lite:latest`

# Mixed Topologies: add a Linux Node

```yaml
# Lesson 1: Mixed topology lab
# One router running srl and one alpine linux host

name: mixed-topology-lab

topology:
  nodes:
    # Router running SRL
    router:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

    # Alpine Linux host
    host1:
      kind: linux
      image: alpine:3.20

  links:
    # Connect router's e1-1 to host1's eth-1
    - endpoints: ["router:e1-1", "host1:eth1"]
```

```sh
# ip addr show eth1
64: eth1@if63: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 9500 qdisc noqueue state UP
    link/ether aa:c1:ab:e0:25:6f brd ff:ff:ff:ff:ff:ff
    inet6 fe80::a8c1:abff:fee0:256f/64 scope link
       valid_lft forever preferred_lft forever
```

# Break/Fix: Container Stopped

```bash
clab deplohy lab.clab.yml
docker stop clab-first-lab-srl2
clab inspect -t lab.clab.yml
```

```bash
# Try to connect to srl2
docker exec -it clab-first-lab-srl2 sr_cli
# ERROR: container is not running

# Inspect shows something wrong
containerlab inspect -t topology/lab.clab.yml
# srl2 shows state: "exited" instead of "running"
```

```bash
docker ps -a --filter name=clab-first-lab
```

(`docker ps` alone would not show the dead container)

Output:
```
CONTAINER ID   IMAGE                           COMMAND                  CREATED         STATUS                       PORTS     NAMES
9b1178a1bca3   ghcr.io/nokia/srlinux:24.10.1   "/tini -- fixuid -q …"   6 minutes ago   Up 6 minutes                           clab-first-lab-srl1
0fa0099ef39c   ghcr.io/nokia/srlinux:24.10.1   "/tini -- fixuid -q …"   6 minutes ago   Exited (143) 3 minutes ago             clab-first-lab-srl2

```


Then `docker start clab-first-lab-srl2`.

# Break/Fix -- Missing Link

Deploy a broken lab

```yaml
name: broken-lab

topology:
  nodes:
    srl1:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

    srl2:
      kind: srl
      image: ghcr.io/nokia/srlinux:24.10.1

  links: []
```

If I do
```bash
$ docker exec -it clab-broken-lab-srl2 sr_cli -c "show interface brief" | head
$ docker exec -it clab-broken-lab-srl1 sr_cli -c "show interface brief" | head
```
The interfaces are shown to have operational state: down. That is because links have no connected endpoints.

Need to add
```yaml
  links:
    - endpoints: ["srl1:e1-1", "srl2:e1-1"]
```

