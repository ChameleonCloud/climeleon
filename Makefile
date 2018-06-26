CC_INSTALL_PATH ?= /usr/local/bin

.PHONY: all
all: install cc-openstack

.PHONY: install
install:
	@ ln -sf $(CURDIR)/bin/* $(CC_INSTALL_PATH)
	@ echo "Installed to $(CC_INSTALL_PATH)."
	@ echo "Set CC_INSTALL_PATH to overwrite this."

# Tool builds

# Get Git versions of individual tools
CC_OPENSTACK_VERSION := $(shell git log -n1 --format=%h -- cc-openstack)

STAMPS := .stamps

define DOCKER_STAMP_RULE
$(1): $(STAMPS)/$(1).docker-$(2)
	touch $$@

$(STAMPS)/$(1).docker-$(2): $(STAMPS)
	cd $(1) && docker build -t $(1) .
	touch $$@
endef

# Docker builds use a rule macro
$(eval $(call DOCKER_STAMP_RULE,cc-openstack,$(CC_OPENSTACK_VERSION)))

$(STAMPS):
	mkdir -p $@
