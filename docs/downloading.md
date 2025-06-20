
```mermaid
start=>start: [H] Select document to fetch
check_local=>condition: [H] Is document available locally?
read_path=>operation: [H] Read LocalFilePath
check_file=>condition: [H] Does file exist?
return_local=>operation: [H] Return file to requesting client
check_remotes=>condition: [H] Are there any Remotes available?
start_remote=>operation: [H] Start Remote Fetch
fail_index=>operation: [H] Return error, initiate indexing
end=>end

start->check_local
check_local(yes)->read_path->check_file
check_file(yes)->return_local->end
check_file(no)->check_remotes
check_local(no)->check_remotes
check_remotes(yes)->start_remote->end
check_remotes(no)->fail_index->end
```
