# FastCampus iOS Programming School API Server

## Requirements

- Docker
- PostgreSQL
- S3 Bucket (Optional)

**Setting files (Create below two files)**  

`.conf-secret/settings_common.json`

> "aws" is optional (If docker run environment contains `MODE=DEBUG`)

```json
{
  "django": {
    "secret_key": "(Django Secret Key)",
    "default_superuser": {
      "username": "(Default Superuser username)",
      "email": "(Default Superuser email)",
      "password": "(Default Superuser password)"
    }
  },
  "aws": {
    "secret_access_key": "(AWS IAM Credential Secret access key)",
    "access_key_id": "(AWS IAM Credential Secret Access key id)",
    "s3_bucket_name": "(AWS S3 Bucket name)",
    "s3_region": "(AWS S3 Bucket region)",
    "s3_signature_version": "(AWS S3 Bucket Signature version)"
  }
}
```

`.conf-secret/settings_local.json`  

```json
{
  "django": {
    "allowed_hosts": [
      "*"
    ]
  },
  "db": {
    "engine": "django.db.backends.postgresql_psycopg2",
    "name": "(DB name)",
    "user": "(DB Owner username)",
    "password": "(DB Owner password)",
    "host": "(DB Host)",
    "port": "(DB Port)"
  }
}
```


## Installation & Run

```
docker build . -t app
docker run -e MODE=DEBUG -p 8000:4567 app
```