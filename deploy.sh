#!/bin/sh

scp bazosrealitydefinitions.py hetzner:/usr/local/bin/
scp bazosrealityspider.py hetzner:/usr/local/bin/

scp bezrealitkyspider.py hetzner:/usr/local/bin/
scp bezrealitkydefinitions.py hetzner:/usr/local/bin/

scp index.html index.js hetzner:/var/www/ivansevcik.cz/r/

ssh hetzner chown www-data:www-data -R /var/www/ivansevcik.cz/r
