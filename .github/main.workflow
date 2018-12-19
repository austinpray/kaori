workflow "Production Deploy" {
  on = "push"
  resolves = [
    "GitHub Action for Google Cloud",
    "make",
  ]
}

action "Google Cloud SDK auth" {
  uses = "actions/gcloud/auth@8ec8bfa"
  secrets = ["GCLOUD_AUTH"]
}

action "GitHub Action for Google Cloud" {
  uses = "actions/gcloud/cli@8ec8bfa"
  needs = ["Google Cloud SDK auth"]
  args = "gcloud components install kubectl"
}

action "make" {
  uses = "actions/docker/cli@76ff57a"
}
