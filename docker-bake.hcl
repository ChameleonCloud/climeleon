# docker-bake.hcl
variable "TAG" {
    default = "latest"
}

group "default" {
    targets = ["chi-docs", "chi-openstack"]
}

target "chi-docs" {
    context = "chi-docs"
    tags = ["docker.chameleoncloud.org/chi-docs:${TAG}"]
    platforms = ["linux/amd64", "linux/arm64"]
}

target "chi-openstack" {
    context = "chi-openstack"
    tags = ["docker.chameleoncloud.org/chi-openstack:${TAG}"]
    platforms = ["linux/amd64", "linux/arm64"]
}