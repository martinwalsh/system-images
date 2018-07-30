include .makefiles/ludicrous.mk

#> Build a packer profile: make (esxi|centos7)

# To prevent the password dialog when Fusion launches ESXi:
# sudo touch /Library/Preferences/VMware\ Fusion/promiscAuthorized

esxi/output-esxi:
	$(call log,building $@)
	cd esxi && packer build $(PACKER_OPTS)  -var-file=vars.json esxi.json

#> build an esxi vm on vmware fusion
esxi: | esxi/output-esxi

#> build a centos7 image on esxi
centos7: | esxi _program_jq
	$(call log,building $@)
	cd $@ && packer build $(PACKER_OPTS) -var "esx_host=$$(jq -r .IPv4Address ../esxi/ipaddress.json)" -var-file=vars.json $@.json

clean:: export PATH := /Applications/VMware\ Fusion.app/Contents/Library/:$(PATH)
clean::
	$(call log,removing build artifacts)
	vmrun stop esxi/output-esxi/esxi.vmx && sleep 10 || true
	rm -rf esxi/{output-*,packer_cache} centos7/{output-*,packer_cache}
	rm -f esxi/ipaddress.json

.PHONY: esxi centos7 clean
