#  Network Types

To join a network, **all parameters and network type must match exactly**.

---

### PeerOnly

**Description:**
The basic network type. Only local entries from paired remotes are synchronized. Synchronizing "Remotes" table from other hosts and recursive download are **not allowed**.

**Parameters:**

* `TTL`: `1`
* `NetworkType`: `PeerOnly`

---

### Public

**Description:**
An extended network type. Synchronizes both local entries and their associated Remotes, enabling deeper recursive discovery across the network.

**Parameters:**

* `TTL`: `20` *(subject to adjustment)*
* `NetworkType`: `Public`
