include .makefiles/ludicrous.mk

#> Build a packer profile: make (esxi|centos7)

# To prevent the password dialog when Fusion launches ESXi:
# sudo touch /Library/Preferences/VMware\ Fusion/promiscAuthorized

ALL := esxi centos7

promisc:
	@if [ ! -f /Applications/VMware\ Fusion.app/Contents/Library/promiscAuthorized ]; then \
		$(call _log,permanently authorize promiscuous mode in VMware Fusion); \
		sudo touch /Applications/VMware\ Fusion.app/Contents/Library/promiscAuthorized ; \
	fi

clean:: export PATH := /Applications/VMware\ Fusion.app/Contents/Library/:$(PATH)
clean::
	$(call log,removing build artifacts)
	for VM in `find . -name "*.vmx"`; do \
		vmrun stop $$VM && sleep 10 || true ; \
	done
	rm -rf build/

#> build all images
build: export PATH := /Applications/VMWare\\ Fusion.app/Contents/Library:$(CURDIR)/bin:$(PATH)
build: | promisc
	for name in $(if $(NAME),$(NAME),$(ALL)); do \
		pipenv run bin/generate $$name; \
		(cd build/$${name} && packer build $(PACKER_OPTS) $${name}.json) ; \
	done

master:
	pipenv run salt-cloud -c salt/etc/salt -m salt/etc/salt/cloud.maps.d/local.conf

.PHONY: build clean promisc
