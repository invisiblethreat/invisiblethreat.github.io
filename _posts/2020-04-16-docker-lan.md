---
layout: post
title: .lan Docker Setup
date:       2020-04-16T08:47:19-04:00
author:     invisiblethreat
thumbnail:  gravatar
summary:    How I leverage Docker on my network
categories: technology
tags:
 - docker
 - ansible
 - containers
---

# `.lan` Docker Setup

Docker is a great way to isolate processes. It also enables shipping things
that are almost fully configured and only require a few variables to be set
along the way

## Tools

* Docker, duh.
* Ansible, because of automation
* Python and `pip` for environment management for Ansible
* `make`. Sorry.
* Git, so you can version all of your Ansible configurations

## Networking Design

![lan.png](/images/lan.png)

When depolying Docker at a network gateway, you get routing for the Docker
networks for free.

### The Docker Network

By default, on Linux, Docker creates the `172.17.0.0/16` network. The addresses
in this space are non-deterministic, which is a non-issue when you're exposing
ports, as it's the host that will weld things together via `docker-proxy`. This
is not desireable for my uses. My goal is to avoid binding ports on the gateway
host if at all possible.

The solution is to make another network that is not the default. I use
`172.18.0.0/16`. This allows for static assignment, which enables DNS and
general sanity to prevail.

### Ansible YAML for creating Docker network

```yaml
- name: Create lan-bridge
  docker_network:
    name: lan-bridge
    ipam_options:
      subnet: 172.18.0.0/16
```

## Management

To keep things portable `virtualenv` is used in conjunction with a `Makefile`.
This permits provisioning of the environment on a new host in short order, with
a few safeguards for secrets.

Both `init` and `end` are sourced, rather than invoked as scripts, to retain
environments after running.

### `init` sets things up

```bash
KEY="auth/ansible-mgmt.key"
make

VAULTID=""

if [ ! -z $VAULTFILE ]; then
  VAULTID="--vault-password-file=$VAULTFILE"
fi

source .ansible/bin/activate

grep -q "BEGIN OPENSSH PRIVATE KEY" $KEY

if [ "$?" -eq "0"  ]; then
  echo "auth/ansible.key is unencrypted. Ready to run playbooks"
else
  echo "auth/ansible.key needs to be decrypted to run playbooks. Running ansible-vault."
  ansible-vault decrypt $VAULTID $KEY
fi

# vim:ft=sh
```

### `Makefile` bootstraps your environment

```make
VIRTUALENV_VERSION=16.3.0
SHELL=/bin/bash
CACHE_DIR=./.cache

# fixes implicit rule converting *.sh to *
.SUFFIXES:

all: .ansible

.PHONY: all clean

.ansible: requirements.txt | $(CACHE_DIR)/virtualenv-$(VIRTUALENV_VERSION)/virtualenv.py
        rm -rf $@
        $(word 1,$|) --no-site-packages $@
        source ./$@/bin/activate; python ./$@/bin/pip install -r $<
        source .ansible/bin/activate

lint: .ansible
        .ansible/bin/python .ansible/bin/ansible-lint plays/compliance/*.yml plays/jobs/*/*.yml
        .ansible/bin/yamllint --strict .
        .ansible/bin/pycodestyle roles resources

$(CACHE_DIR):
        mkdir -p $@

$(CACHE_DIR)/virtualenv-$(VIRTUALENV_VERSION)/virtualenv.py: $(CACHE_DIR)/virtualenv-$(VIRTUALENV_VERSION).tar.gz
        tar -xzf $< -C $(<D)
        touch $@ # this ensures this target doesn't get continually re-run

$(CACHE_DIR)/virtualenv-$(VIRTUALENV_VERSION).tar.gz: $(CACHE_DIR)
        curl -o $@ -L https://pypi.io/packages/source/v/virtualenv/virtualenv-$(VIRTUALENV_VERSION).tar.gz

clean:
        rm -rf .ansible
```

### `end` protects us from ourselves

```bash
# This is the file that will be used to run vault. If it is not set, vault
# will prompt for a password. It is controlled in this manner due to the
# syntax that an assignement string as an argument.
VAULTID=""

# Look for the export of
if [ ! -z $VAULTFILE ]; then
  echo "Using $VAULTFILE for vault commands"
  VAULTID="--vault-password-file=$VAULTFILE"
else
  echo "\$VAULTFILE not set- will prompt for vault password"
fi

# These files should never be committed unencrypted
files=(auth/ansible-mgmt.key roles/docker/wiki/vars/main.yml roles/docker/pihole/vars/main.yml)

for file in ${files[@]}
do
    # Check to see if the file has the vault header
    grep -q "ANSIBLE_VAULT" $file

    if [ "$?" -eq "1"  ]; then
      echo "$file is unencrypted. It needs to be encrypted before you're done."
      ansible-vault encrypt $VAULTID $file
    else
      echo "$file is encrypted."
    fi
done

# Get out of the virtualenv
deactivate

# Disable the zsh "no matches found" option. We will have to now redirect
# STDERR for the 'ls' comannd
setopt +o nomatch

# Cleanup stray 'retry' files from runs that have partially failed
for i in $(ls plays/*.retry 2>/dev/null)
do
  echo -n "Removing $i... "
  rm -rf $i
  echo "Done."
done

# Re-enable nomatch
setopt -o nomatch
# vim:ft=sh
```

## Example Service: PiHole

```
pihole
├── README.md
├── tasks
│   └── main.yml
└── vars
    └── main.yml
```

### `tasks/main.yml`

```yaml
{% raw %}
- name: "Pull {{ ctname }} Image"
  docker_image:
    name: "{{ ctname }}/{{ ctname }}"
    tag: latest
    pull: yes

- name: Include Common Runtime Variables
  include_vars:
    dir: ../../vars/

- name: "Run {{ ctname }}"
  docker_container:
    name: "{{ ctname }}"
    hostname: "{{ ctname }}"
    image: "{{ ctname }}/{{ ctname }}"
    pull: yes
    state: started
    restart: yes
    restart_policy: always
    capabilities:
      - NET_ADMIN
    dns_servers:
      - 127.0.0.1
      - 8.8.8.8
    purge_networks: yes
    networks:
      - name: "{{ bridge }}"
        ipv4_address: "{{ ipaddr }}"
    env:
      ServerIP: "{{ ipaddr }}"
      PUID: "{{ media.uid }}"
      PGID: "{{ media.gid }}"
      TZ: "{{ tz.local }}"
      WEBPASSWORD: "{{ piholepass }}"
    volumes:
      - "{{ media.container }}/{{ ctname }}:/etc/{{ ctname }}:rw"
      - "{{ media.container }}/{{ ctname }}/dnsmasq.d/:/etc/dnsmasq.d:rw"
      - "/etc/localtime:/etc/localtime:ro"
      - "/dev/rtc:/dev/rtc:ro"
{% endraw %}
```

Note: DNS servers are important. `127.0.0.1` ensures that Pihole works, and 
`8.8.8.8` ensures that the container has fallback to the real internet if
something goes wrong

### `vars/main.yml`

```yaml
ctname: pihole
ipaddr: 172.18.0.2
```

### `../../vars/` Common variables to all containers

```yaml
bridge: lan-bridge
media:
  home: /home/media
  container: /home/media/container
  uid: 1001
  gid: 1002
tz:
  local: "America/Halifax"
env:
  PUID: "media"
  PGID: "media"
volumes:
  - "/etc/localtime:/etc/localtime:ro"
  - "/dev/rtc:/dev/rtc:ro"
  ```
