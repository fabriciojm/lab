# Container Networking

Containers use netnamespaces to manage their networking. Both containers hosted in a system and the bridge that routes the information to them need virtual interfaces (veth) and a virtual connection between them (veth pair).

```bash
sudo ip netns add <namespace-name>
```


