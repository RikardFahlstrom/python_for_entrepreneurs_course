#!/bin/bash
ansible-playbook -vvvv ./deploy.yml --private-key=/Users/Rikard/Documents/ssh_keys/do_deploy -u deployer -i ./hosts
