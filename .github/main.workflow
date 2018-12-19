workflow "Production Deploy" {
  on = "push"
  resolves = [
    "make",
  ]
}

action "make" {
  uses = "actions/docker/cli@76ff57a"
  runs = "apk add --update make && make"
}
