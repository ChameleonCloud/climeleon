CHI_INSTALL_PATH ?= /usr/local/bin
DOCKER_REGISTRY ?= docker.chameleoncloud.org
DOCKER_FLAGS ?=
ARCH_TAG ?= $(shell arch)

CONTAINERS := chi-docs chi-openstack

.PHONY: all
all: build install

.PHONY: build
build: $(CONTAINERS)

.PHONY: publish
publish: $(CONTAINERS:%=%-publish)

.PHONY: install
install:
	@ echo "Linking to $(CHI_INSTALL_PATH). Set CHI_INSTALL_PATH to override this."
	@ ln -sf $(CURDIR)/bin/* $(CHI_INSTALL_PATH) 2>/dev/null || sudo ln -sf $(CURDIR)/bin/* $(CHI_INSTALL_PATH)

# Tool builds
STAMPS := .stamps

$(STAMPS):
	mkdir -p $@

define container_rule
$(eval VERSION := $(shell git log -n1 --format=%h -- $(1)))
$(eval IMAGE := $(DOCKER_REGISTRY)/$(1)-$(ARCH_TAG))

$(1): $(STAMPS)/$(1).docker-$(VERSION)-$(ARCH_TAG)
	touch $$@

.PHONY: $(1)-publish
$(1)-publish: $(1)
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

$(STAMPS)/$(1).docker-$(VERSION)-$(ARCH_TAG): $(STAMPS)
	cd $(1) && docker build $(DOCKER_FLAGS) -t $(IMAGE):$(VERSION) .
	docker tag $(IMAGE):$(VERSION) $(IMAGE):latest
	touch $$@
endef

# Docker builds use a rule macro
$(foreach name, $(CONTAINERS), $(eval $(call container_rule,$(name))))
