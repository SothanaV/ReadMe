# Open Stack
## install
    sudo apt update -y && sudo apt upgrade -y
    sudo adduser stack --disabled-password
    echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
    su - stack
    sudo apt install git -y
    git clone https://git.openstack.org/openstack-dev/devstack
    cd devstack
    
## add local.conf

    [[local|localrc]]

    # Password for KeyStone, Database, RabbitMQ and Service
    ADMIN_PASSWORD=StrongAdminSecret
    DATABASE_PASSWORD=$ADMIN_PASSWORD
    RABBIT_PASSWORD=$ADMIN_PASSWORD
    SERVICE_PASSWORD=$ADMIN_PASSWORD

    # Host IP - get your Server/VM IP address from ip addr command
    HOST_IP=<server ip address>


    ./stack.sh