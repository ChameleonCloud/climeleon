CC_INSTALL_PATH ?= /usr/local/bin

STAMPS = .stamps

.PHONY: install
install:
	ln -s $(CURDIR)/bin/cc $(CC_INSTALL_PATH)/cc

cc-openstack: $(STAMPS)/cc-openstack

$(STAMPS)/cc-openstack: $(STAMPS)
	cd $(notdir $@) && docker build -t $(notdir $@) .
	touch $@

$(STAMPS):
	mkdir -p $@
