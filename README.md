# F.L.A.S.Z.K.

**Fajne Lingwistyczne Archiwum Sekretów Zapisane Komputerowo** — an application for creating a distributed database of documents.

This web app may change the way you share files between devices. Curious how?  
Let’s walk through all the features, in the order they’re used while setting up the app.

---

## 1. Indexing

- On the **Settings** page, choose the folder that contains the files you want to index.  
- Then click the **Indexing** button in the menu — all your files will appear.  
- Clicking on a file card lets you view its **metadata** and **description**.

---

## 2. Pairing

- On the **Settings** page, you'll find a **Generate PIN** button and a form with fields:  
  - IP  
  - PIN  
  - **Start Pairing** button  
- The next step is to generate a PIN on the device with the indexed files, and enter that PIN on the device you wish to synchronize.  
- To securely pair devices, a secret is exchanged — later used during synchronization.  
  To achieve this securely, we’ve implemented the [Three-pass protocol](https://en.wikipedia.org/wiki/Three-pass_protocol) using sockets.

---

## 3. Synchronization

- After completing the previous steps, just click the **Sync** button — *voilà!*  
  Everything appears alongside your original files and is ready for download.  
- The exact synchronization process is described [here](https://github.com/Crowfunder/flaszk/blob/main/docs/synchronization.md).

---

## Final Notes

Have fun exploring this new way of sharing your files —  
and remember to leave us some feedback!
