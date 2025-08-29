# Python connect smb
- install package
```bash
pip install fsspec smbprotocol duckdb smbclient
```

- using fsspec fs
```python
import fsspec

fs = fsspec.filesystem(
    "smb",
    username="domain\\User",
    password="Password",
    host="server.local",
)
fs.ls('')
```

- using with duckdb
```python
import duckdb
import smbclient
from fsspec.implementations.smb import SMBFileSystem
from stat import S_ISDIR, S_ISLNK

protocol = "mysmb"

def _as_unc_path(host, path):
    rpath = path.replace("/", "\\").replace(f"{protocol}:\\", "")
    unc = f"\\\\{host}{rpath}"
    print(unc)
    return unc

class MySMBFileSystem(SMBFileSystem):
    protocol = protocol

    def info(self, path, **kwargs):
        wpath = _as_unc_path(self.host, path)
        stats = smbclient.stat(wpath, port=self._port, **kwargs)
        if S_ISDIR(stats.st_mode):
            stype = "directory"
        elif S_ISLNK(stats.st_mode):
            stype = "link"
        else:
            stype = "file"
        res = {
            "name": path + "/" if stype == "directory" else path,
            "size": stats.st_size,
            "type": stype,
            "uid": stats.st_uid,
            "gid": stats.st_gid,
            "time": stats.st_atime,
            "mtime": stats.st_mtime,
        }
        return res
fsspec.register_implementation("mysmb", MySMBFileSystem)

fs = fsspec.filesystem(
    "mysmb",
    username="domain\\User",
    password="Password",
    host="server.local",
)



def query_duck(query):
    con = duckdb.connect()
    con.register_filesystem(fs)
    r = con.sql(query)
    return r.df() if r != None else r

query_duck(r"""
    SELECT * 
    FROM read_csv_auto("mysmb:///Data/Landing/*.csv")
    LIMIT 5
""")
```