# Google Cloud Storage Bucket CORS Configuration

This guide explains how to configure Cross-Origin Resource Sharing (CORS) on a Google Cloud Storage bucket.

## Prerequisites

- Google Cloud SDK (`gsutil`) installed, or access to the GCP Cloud Shell
- Sufficient permissions on the target bucket (Storage Admin or Storage Legacy Bucket Owner)

## Steps

### 1. Open the Terminal

Log in to the GCP Console and open Cloud Shell, or use a local terminal with the Google Cloud SDK authenticated.

### 2. Create the CORS Configuration File

Create a file named `cors-config.json` with the desired CORS policy:

```bash
echo '[{"origin": ["*"],"responseHeader": ["Content-Type"],"method": ["GET", "HEAD"],"maxAgeSeconds": 3600}]' > cors-config.json
```

The configuration above allows:

- **Origins:** all origins (`*`)
- **Response headers:** `Content-Type`
- **Methods:** `GET` and `HEAD`
- **Max age:** 3600 seconds (1 hour) for preflight cache

For production environments, replace `"*"` with specific allowed origins, for example:

```json
[
  {
    "origin": ["https://example.com"],
    "responseHeader": ["Content-Type", "Authorization"],
    "method": ["GET", "HEAD", "POST"],
    "maxAgeSeconds": 3600
  }
]
```

### 3. Apply the CORS Configuration

```bash
gsutil cors set cors-config.json gs://<BUCKET_NAME>
```

Replace `<BUCKET_NAME>` with the name of your bucket.

### 4. Verify the Applied Configuration

```bash
gsutil cors get gs://<BUCKET_NAME>
```

The command should return the CORS configuration you applied.

## Notes

- CORS settings apply at the bucket level, not at the object level.
- Changes take effect immediately but may be cached by browsers according to `maxAgeSeconds`.
- To remove CORS configuration entirely, apply an empty array: `echo '[]' > cors-config.json` and re-run the `set` command.
