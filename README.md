# system-images

This project is an experiement using packer, esxi and salt, to bootstrap a local development
environment for creating system images.

## Requirements

* [VMWare Fusion](https://www.vmware.com/products/fusion/fusion-evaluation.html) or [VMWare
  Workstation](https://www.vmware.com/products/workstation-pro/workstation-pro-evaluation.html)
* [packer](https://www.packer.io/intro/getting-started/install.html)
* [jq](https://github.com/stedolan/jq/wiki/Installation)
* [ESXi iso](https://my.vmware.com/en/web/vmware/evalcenter?p=free-esxi6)

## Steps

1. Create a `vars.json` in each build directory (`esxi/`, `centos7`, etc) from the corresponding
   `vars.json.example` provided.
2. Run `make centos7`

## Cleanup

Run `make clean`.

NOTE: This will destroy all running vms and their build artifacts.

## See Also

* [packer documentation](https://www.packer.io/docs/index.html)
* [frapposelli/esxi-packer-templates](https://github.com/frapposelli/esxi-packer-templates)
* [boxcutter/esxi](https://github.com/boxcutter/esxi)
* [nickcharlton/packer-esxi](https://github.com/nickcharlton/packer-esxi)
* [geerlingguy/packer-centos-7](https://github.com/geerlingguy/packer-centos-7)
