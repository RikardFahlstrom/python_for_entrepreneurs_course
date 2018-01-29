#!/bin/bash
ansible-playbook -vvvv ./init_config.yml --private-key=/Users/Rikard/Documents/ssh_keys/do_deploy -u root -i ./hosts