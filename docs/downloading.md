# Download Algorithm

## Local Fetch – `LocalFetch`

```mermaid
flowchart TD
    A[[Start: Select document to fetch]]
    B{Is document available locally?}
    C[Read LocalFilePath]
    D{Does file exist?}
    E[Return file to requesting client]
    F{Are there any Remotes available?}
    G[Start Remote Fetch]
    H[Return error, initiate indexing]
    Z[[End]]

    A --> B
    B -- Yes --> C --> D
    D -- Yes --> E --> Z
    D -- No --> F
    B -- No --> F
    F -- Yes --> G --> Z
    F -- No --> H --> Z
```

---

## Remote Fetch – PeerOnly Network

```mermaid
flowchart TD
    A[[Start: Iterate over Document.Mirrors]]
    B[Send fetch request with Secret & FileHash]
    C[On Remote: Find document by FileHash in Index]
    D{Is document available locally on Remote?}
    E[Remote returns document to Host]
    F[Remote returns 404 to Host]
    G{Did Host receive document?}
    H[Verify checksum, return to requester]
    I{More Remotes to try?}
    J[Try next Remote]
    K[Return 404: Document not found]

    A --> B --> C --> D
    D -- Yes --> E --> G
    D -- No --> F --> G
    G -- Yes --> H
    G -- No --> I
    I -- Yes --> J --> B
    I -- No --> K
```

## Remote Fetch – Public Network
```mermaid
flowchart TD
    A[[Start: Iterate over Document.Remotes]]
    B[Send fetch request with Secret & FileHash]
    C[On Remote: Find document by FileHash]
    D{Is file available locally on Remote?}
    E[Perform Local Fetch on Remote]
    F[Start Recursive Remote Fetch]
    G[If received: buffer, verify checksum, return to Host]
    H[Host verifies checksum, return to original requester]
    I{More Remotes to try?}
    J[Try next Remote]
    K[Return 404 file not found]

    A --> B --> C --> D
    D -- Yes --> E --> G --> H 
    D -- No --> F --> A
    G --> H 
    B --> I
    I -- Yes --> J --> B
    I -- No --> K 


```

---

## Notes

* **TTL (Time To Live)**/**Hops** should be part of the download request. If it goes over the limit, return 404.
* If **Remote is inaccessible** (timeout), skip it and try another. Return `404` only when all available remotes are used up.
