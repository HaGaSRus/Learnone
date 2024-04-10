#!/bin/bash

export WEBROOT_PATH=/var/www/certbot/
export EMAIL=tro37295@gmail.com
export DOMAIN=learnone.ru

certbot certonly --webroot --webroot-path=$WEBROOT_PATH --email "$EMAIL" --agree-tos --no-eff-email -d "$DOMAIN" -d "www.$DOMAIN"
~                                                                                                                           ~                                                                                                                           ~              
