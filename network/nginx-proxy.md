# Nginx Proxy
- create `nginx.conf`
```conf
map $http_upgrade $connection_upgrade {
  default upgrade;
  ''      close;
}

upstream backend {
    server 192.168.24.10:8006;
}

server {
    listen 8000;
    listen [::]:8000;

    server_name _;
    client_max_body_size 0;

    location / {
        proxy_pass https://backend/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-Proto https;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;        
        
        proxy_ssl_server_name on;
        proxy_ssl_name 192.168.24.10;
        proxy_ssl_verify off;
        
        proxy_read_timeout 3600;
        proxy_send_timeout 3600;
    }

}
```
- create `docker-compose.yml`
```yml
services: 
    nginx:
        container_name: nginx
        image: nginx:1.25.2-alpine
        ports:
            - 8000:8000
        volumes:
            - ./config/nginx.conf:/etc/nginx/conf.d/default.conf
        environment:
            NGINX_ENVSUBST_TEMPLATE_SUFFIX: ".conf"
```

- run service
```sh
docker-compose up
```