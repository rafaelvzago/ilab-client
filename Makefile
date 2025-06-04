.PHONY: build push clean help

# Variables
IMAGE_NAME ?= ilab-client
IMAGE_TAG ?= latest
REGISTRY ?= 

# Build Podman image
build:
	podman build -f Dockerfile -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Build and tag with registry
build-registry:
	podman build -f Dockerfile -t $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG) .

# Push image to registry
push: build-registry
	podman push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

# Clean up local images
clean:
	podman rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	podman rmi $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG) || true

# Show help
help:
	@echo "Available targets:"
	@echo "  build          - Build Podman image locally"
	@echo "  build-registry - Build and tag with registry prefix"
	@echo "  push           - Build and push to registry"
	@echo "  clean          - Remove local Podman images"
	@echo "  help           - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  IMAGE_NAME     - Podman image name (default: ilab-client)"
	@echo "  IMAGE_TAG      - Podman image tag (default: latest)"
	@echo "  REGISTRY       - Container registry prefix (e.g., docker.io/username)"