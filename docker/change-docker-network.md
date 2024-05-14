# Change Default docker network
- in some time want to connect service(s) via IP but conflit with docker default IP(s)

## defaul ip pools subnet
-  add code command
```
nano /etc/docker/daemon.json
```
- copy & paste this
```json
{
  "default-address-pools":
  [
    {"base":"10.10.0.0/16","size":24}
  ]
}
```
- restart docker services
```
service docker restart
```

- test subnet chagnged

```
docker network create foo
docker network inspect foo | grep Subnet
```
output
```
"Subnet": "10.10.1.0/24"
```
