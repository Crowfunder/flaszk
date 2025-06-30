# Indexing and parsing metadata of local documents
1. Load parsers into dict mapping filetype to Callable.
2. Iterate over all folder paths that are defined in configs.
3. Iterate recursively over all files and subfolders in said folder.
4. Call importLocalDocument() function and index the file.
5. Check if file type is in list of available types.
6. If it is, call the parser method, create new DocumentMetadata object.