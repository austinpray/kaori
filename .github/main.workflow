workflow "New workflow" {
  on = "push"
  resolves = ["assets build"]
}

action "node modules" {
  uses = "actions/npm@de7a3705a9510ee12702e124482fad6af249991b"
  runs = "npm ci"
}

action "assets build" {
  uses = "actions/npm@de7a3705a9510ee12702e124482fad6af249991b"
  runs = "npm run build"
  needs = ["node modules"]
}
