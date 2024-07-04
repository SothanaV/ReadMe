# Gen Copy SetNoPass SSH to server
- gen key
```
ssh-keygen -t rsa -b 4096 -f "<PATH/KEYNAME>" -N ""
```
- copy key to server
```
ssh-copy-id -i <KEY>.pub <USERNMAE>@<HOST>
```
- ssh to server
```
ssh -i <KEY> <USERNMAE>@<HOST>
```
- set no pass
```
echo "$USER    ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
```