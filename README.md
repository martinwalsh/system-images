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

1. Download the [ESXi iso](https://www.vmware.com/go/get-free-esxi) to any location under the root of this project.
2. Make note of the checksum and license code from the download page.
2. Run `make build` and respond to prompts, as necessary.

## Iterative Builds

Pass a NAME parameter to `make build`. For example ...

```
make build NAME=centos7
```

... this will skip the esxi build, assuming it has already completed.

## Cleanup

Run `make clean`.

NOTE: This will destroy all running vms and their build artifacts.

## See Also

* [packer documentation](https://www.packer.io/docs/index.html)
* [frapposelli/esxi-packer-templates](https://github.com/frapposelli/esxi-packer-templates)
* [boxcutter/esxi](https://github.com/boxcutter/esxi)
* [nickcharlton/packer-esxi](https://github.com/nickcharlton/packer-esxi)
* [geerlingguy/packer-centos-7](https://github.com/geerlingguy/packer-centos-7)
