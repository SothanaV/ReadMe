# Google Cloud Bucket
1. go to gcp console
2. open terminal
3. create config

```
echo '[{"origin": ["*"],"responseHeader": ["Content-Type"],"method": ["GET", "HEAD"],"maxAgeSeconds": 3600}]' > cors-config.json
```

4. apply config

    ```
    gsutil cors set cors-config.json gs://<BUCKET_NAME>
    ```

5. check applyed config
    ```
    gsutil cors get gs://<BUCKET_NAME>
    ```

