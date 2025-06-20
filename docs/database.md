# Database Schema

## Tables Overview

* **Index** – Book index
* **Remotes** – Paired servers
* **Metadata** – Book metadata

---

## Models

### 📄 Document (in `Index` table)

| Field           | Type           | Description                                       |
| --------------- | -------------- | ------------------------------------------------- |
| `LocalId`       | `Int`          | Local identifier of the document                  |
| `FileHash`      | `String?`      | Optional hash of the file                         |
| `LocalFilePath` | `String?`      | Optional path to the local file, if applicable                   |
| `isLocal`       | `Bool`         | Indicates whether the document is available locally  |
| `Metadata`      | → Foreign Key  | Reference to associated metadata                  |
| `Remotes`       | `List<Remote>` | Back-propagated list of associated remote servers |

---

### 🌐 Remote (in `Remotes` table)

| Field     | Type      | Description                     |
| --------- | --------- | ------------------------------- |
| `Id`      | `Int`     | Unique identifier of the remote |
| `Address` | `String`  | Server address                  |
| `Port`    | `Int`     | Communication port              |
| `Secret`  | `String`  | Authentication secret           |
| `Name`    | `String?` | Optional name of the server     |

---

### 🧾 Metadata (in `Metadata` table)

> **TBD** – Structure to be defined


