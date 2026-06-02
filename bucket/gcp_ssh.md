# GCP Cloud Shell SSH

Connect to the GCP Cloud Shell environment directly from the command line using the Google Cloud SDK.

## Prerequisites

- Google Cloud SDK (`gcloud`) installed and authenticated
- An active GCP project selected

## Connect to Cloud Shell

```bash
gcloud cloud-shell ssh
```

This command opens an SSH session to your personal Cloud Shell instance. The Cloud Shell environment is a temporary virtual machine provisioned by Google with common development tools pre-installed.

## Notes

- Cloud Shell sessions are ephemeral; persistent storage is limited to the `$HOME` directory (5 GB).
- If your Cloud Shell instance is inactive it may be reclaimed; running the command again provisions a new one.
- To transfer files to or from Cloud Shell, use `gcloud cloud-shell scp`.
