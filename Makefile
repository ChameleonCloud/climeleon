CHI_INSTALL_PATH ?= /usr/local/bin
DOCKER_REGISTRY ?= docker.chameleoncloud.org
DOCKER_FLAGS ?=
ARCH_TAG ?= $(shell arch)

.PHONY: all
all: build install

.PHONY: build
build:
	docker buildx bake --pull

.PHONY: publish
publish:
	docker buildx bake --pull --push

.PHONY: install
install:
	@ echo "Linking to $(CHI_INSTALL_PATH). Set CHI_INSTALL_PATH to override this."
	@ ln -sf $(CURDIR)/bin/* $(CHI_INSTALL_PATH) 2>/dev/null || sudo ln -sf $(CURDIR)/bin/* $(CHI_INSTALL_PATH)
