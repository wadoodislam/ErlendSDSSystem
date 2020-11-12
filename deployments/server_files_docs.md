# scrapyd.conf
This file is a configuration file for scrapyd process.

*command*: `sudo less /etc/scrapyd/scrapyd.conf`

*location*: `/etc/scrapyd`

```editorconfig
[scrapyd]

max_proc=30
debug=on
bind_address=0.0.0.0
```

# crontab
This file specifies the system commands and rotines that are set to run periodically.

*command*: `EDITOR=nano crontab -e`

*location*: `/etc/scrapyd`

##### content
```shell script
PATH=/home/ubuntu/venv/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/ubuntu/.local/bin:/home/ubuntu/bin

@reboot nohup scrapyd >& /dev/null &
@reboot uwsgi --ini /etc/uwsgi/netpower-uwsgi.ini > /tmp/uwsgi_reboot.log
@reboot sudo service nginx start > /tmp/nginx_reboot.log

* * * * *   python ErlendSDSSystem/sds_system/manage.py runcrons > /tmp/django_cron.log 2>&1
00 18 * * * bash ErlendSDSSystem/deployments/deploy_scrapyd.sh > /tmp/deploy_scrapyd.log 2>&1
```

# netpower_nginx.conf

This file is a configuration file for nginx server.

*command*: `sudo less /etc/scrapyd/scrapyd.conf`

*location*: `/etc/scrapyd`

```editorconfig
[scrapyd]

max_proc=30
debug=on
bind_address=0.0.0.0
```
