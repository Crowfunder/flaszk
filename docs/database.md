# Database Schema

## Tables Overview

* **Documents** – Documents index
* **Remotes** – Paired servers
* **Metadata** – Book metadata

---

## Models

### Document (in `documents` table)

| Field                  | Type                                 | Description                                                             |
| ---------------------- | ------------------------------------ | ----------------------------------------------------------------------- |
| `file_hash`            | `String`                             | Primary Key. Hash of the file used for identification (e.g., SHA-256).      |
| `file_path`      | `String?`                             | Optional local file path if the file is available locally.             |
| `is_local`             | `Boolean`                            | Indicates whether the file is stored locally (`True`) or only mirrored. |
| `document_metadata_id` | `Integer`                            | Foreign key to `documents_metadata.Id`, links to associated metadata.   |
| `mirrors`              | `Relationship[List[DocumentMirror]]` | All remote mirrors storing this document.                               |


---

### Remote (in `remotes` table)

| Field     | Type                                 | Description                                            |
| --------- | ------------------------------------ | ------------------------------------------------------ |
| `Id`      | `Integer`                            | Primary key. Unique ID of the remote.                  |
| `address` | `String`                             | Host or IP address of the remote server.               |
| `port`    | `Integer`                            | Network port used by the remote server.                |
| `secret`  | `String`                             | Secret token used for authentication with remote. |
| `name`    | `String?`                            | Optional human-readable name for the remote server.    |
| `mirrors` | `Relationship[List[DocumentMirror]]` | Documents mirrors on this remote server.              |


---

### DocumentMirror (in `documents_mirrors` table)
| Field         | Type                     | Description                                                                    |
| ------------- | ------------------------ | ------------------------------------------------------------------------------ |
| `Id`          | `Integer`                | Primary key. Unique ID of the mirror entry.                                    |
| `document_Id` | `Integer`                | Foreign key to `documents.local_Id`. Links to the mirrored document.           |
| `remote_Id`   | `Integer`                | Foreign key to `remotes.Id`. Links to the remote where the document is hosted. |

---

### DocumentMetadata (in `documents_metadata` table)
> **TBD** – Structure to be defined

| Field         | Type                     | Description                                                        |
| ------------- | ------------------------ | ------------------------------------------------------------------ |
| `Id`          | `Integer`                | Primary key. Unique metadata entry ID.                             |
| `document_Id` | `Integer`                | Foreign key to `documents.local_Id`. Links metadata to a document. |

---


