;
; BIND data file for projetofrc.com
;
$TTL    604800
@       IN      SOA     projetofrc.com. root.projetofrc.com. (
                        3121705         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@		IN      NS      projetofrc.com.
projetofrc.com.	IN	A	127.0.1.1             
