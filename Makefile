CHI_INSTALL_PATH ?= /usr/local/bin
DOCKER_REGISTRY ?= docker.chameleoncloud.org
DOCKER_FLAGS ?= --platform "linux/amd64,linux/arm64"

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
$(eval IMAGE := $(DOCKER_REGISTRY)/$(1))

$(1): $(STAMPS)/$(1).docker-$(VERSION)
	touch $$@

$(STAMPS)/$(1).docker-$(VERSION): $(STAMPS)
	cd $(1) && docker buildx build $(DOCKER_FLAGS) --tag $(IMAGE):$(VERSION) --tag $(IMAGE):latest --pull --push .

# Docker builds use a rule macro
$(foreach name, $(CONTAINERS), $(eval $(call container_rule,$(name))))
