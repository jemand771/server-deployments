# server-deployments
A collection of kubernetes yaml definitions to deploy to my cluster. Config will be synced automatically.

## Workflow
When a new commit is pushed to this repo's default branch (`main`), [argocd](https://argo-cd.readthedocs.io/en/stable/) will pick it up within a couple of minutes.
Depending on the configuration for each app, changes will either be synced to my cluster automatically or wait for me to manually sync them.
As a rule of thumb: apps that don't cause disruptions when restarting/updating are set to auto-sync while anything that would cause noticable downtime is limited to manual sync.
The latter group includes things like game servers and critical infrastructure. You can always check the app definitions to see which policy applies.

This repo also makes use of [renovate](https://github.com/renovatebot/renovate) to automate docker image updates.
Renovate will periodically check some hand-picked apps and create pull requests if new image versions are available.

Merged pull requests will be commented by a [GitHub bot](https://github.com/int128/argocd-commenter) when their sync/health status changes.
Please note that that setup is still kinda wonky, so sorry in advance if it spams you with PR comments.

## Repo structure

Every folder in this repo represents one application. Some apps I consider important have their folders within `_infrastructure/`, although that folder scheme has slightly fallen apart over time.

The argocd folder includes manifests for the argo apps themselves. This isn't ideal because sometimes auto-sync gets in the way of manual edits submitted to the cluster. I'm currently working on a way to prevent that.

## Questions/Further info

If you have questions about anything in this repo, feel free to open a new issue and ask. You don't have to be too formal, however, please use common sense: Try to research yourself first, and if you decide to open an issue, please write it in a way that makes answering it low effort for me.

Also note that I probably won't be able to help troubleshoot your specific setup if I don't already know you. If I do, just DM me on discord and I'll see what I can do :)

## Contributions

While PRs are welcome, please check back with me before trying to PR any non-trivial changes. This is just a time-saving measure for everyone involved, since I probably won't accept it if I don't agree with the change. (Can't have randoms fiddling with my cluster, lol)

## Security

If you find something in this repo that's not supposed to be here and might be security-critical (such as unencrypted secrets, tokens, ...) or any other kind of vulnurability/critical misconfiguration, please disclose privately to `security@jemand771.net`.
