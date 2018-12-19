workflow "Production Deploy" {
  on = "push"
  resolves = [
    "make",
  ]
}

action "make" {
  uses = "actions/docker/cli@76ff57a"
  args = "sh -c  'apk add --update make && make'"
}
