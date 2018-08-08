CC_INSTALL_PATH ?= /usr/local/bin

.PHONY: all
all: install cc-docs cc-openstack cc-rpm

.PHONY: install
install:
	@ ln -sf $(CURDIR)/bin/* $(CC_INSTALL_PATH)
	@ echo "Installed to $(CC_INSTALL_PATH)."
	@ echo "Set CC_INSTALL_PATH to overwrite this."

# Tool builds
STAMPS := .stamps

container_version = $(shell git log -n1 --format=%h -- $(1))
define container_rule
$(1): $(STAMPS)/$(1).docker-$(call container_version,$(1))
	touch $$@

$(STAMPS)/$(1).docker-$(call container_version,$(1)): $(STAMPS)
	cd $(1) && docker build -t $(1) .
	touch $$@
endef

# Docker builds use a rule macro
$(eval $(call container_rule,cc-docs))
$(eval $(call container_rule,cc-openstack))
$(eval $(call container_rule,cc-rpm))

$(STAMPS):
	mkdir -p $@
