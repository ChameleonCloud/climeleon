CC_INSTALL_PATH ?= /usr/local/bin

REGISTRY := docker.chameleoncloud.org

CONTAINERS := cc-docs cc-openstack cc-rpm

.PHONY: all
all: install $(CONTAINERS)

.PHONY: publish
publish: $(CONTAINERS:%=%-publish)

.PHONY: install
install:
	@ ln -sf $(CURDIR)/bin/* $(CC_INSTALL_PATH)
	@ echo "Installed to $(CC_INSTALL_PATH)."
	@ echo "Set CC_INSTALL_PATH to overwrite this."

# Tool builds
STAMPS := .stamps

$(STAMPS):
	mkdir -p $@

define container_rule
$(eval VERSION := $(shell git log -n1 --format=%h -- $(1)))
$(eval IMAGE := $(REGISTRY)/$(1))

$(1): $(STAMPS)/$(1).docker-$(VERSION)
	touch $$@

.PHONY: $(1)-publish
$(1)-publish: $(1)
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

$(STAMPS)/$(1).docker-$(VERSION): $(STAMPS)
	cd $(1) && docker build -t $(IMAGE):$(VERSION) .
	docker tag $(IMAGE):$(VERSION) $(IMAGE):latest
	touch $$@
endef

# Docker builds use a rule macro
$(foreach name, $(CONTAINERS), $(eval $(call container_rule,$(name))))
