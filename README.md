# Smart Gateway Project

## Requirements

- Node
- Docker
- Docker Compose

## Installation

1. Install node packages for consumer frontend:

```bash
cd consumer-frontend
npm i 
```

2. Install node packges for producer frontend:
```bash
cd producer-frontend
npm i
```
3. Start docker compose:

```bash
docker-compose up -d 
```

## Important URLs:

- https://consumer.tenant.lan:8443
- https://producer.smartland.lan
- https://auth.smartland.lan

## Set up Authentik

### Login: [Authentik](https://auth.smartland.lan "Authentik Login")

```bash
akadmin:akadmin 
```

> is something wrong, lock at Troubleshooting 

### Admin Interface

![Authentik-Akadmin](/images-readme/admin-interface.jpeg)

### Create OAuth2/Open-ID-Provider:

>Applications > Providers > Create

![Authentik-Provider1](/images-readme/new-provider.jpeg)
![Authentik-Provider2](/images-readme/new-provider-2.jpeg)
![Authentik-Provider3](/images-readme/new-provider-3.jpeg)
![Authentik-Provider4](/images-readme/new-provider-4.jpeg)
![Authentik-Provider5](/images-readme/new-provider-5.jpeg)

>Copy "Client ID" and "Client Secret" to `producer-backend/.env`

### Create Application and bind to provider:

>Applications  > Create

![Authentik-Application](/images-readme/new-application.jpeg)

### Create User for Application:

>Directory > Users > users > create

![Authentik-User](/images-readme/create-user.jpeg)

### Set password for user (producer1):

>Click at user

![Authentik-Userpassword](/images-readme/set-user-password.jpeg)

### Bind User to Application:

>Application > producer > Policy/Group/User Bindings > Bind existing Policy/Group/User

![Authentik-Bind-User](/images-readme/bind-user-to-application.jpeg)


## Troubleshooting

### Authentik

#### I can't log in to authentik

```bash
docker exec -it smart-gateway-worker-1 bash
```

```bash
ak create_recovery_key 10 akadmin
```

>copy "RECOVERY-LINK" for authentication without password

>call: https://auth.smartland.lan/RECOVERY-LINK

>set new password for akadmin
https://auth.smartland.lan/recovery/use-token/2GPB7H5G6oZlY0T9cWeTMFBYqTswwCVHL2FDjDgzHuY8SxalsapjKyfyKd7s/

curl --insecure -L -X POST https://producer.smartland.lan/api/home/add -H "Authorization: Basic consumer1:bmZhyTDbsbxU3wufj6vtztMIlEr9fFIUkzfSWGCaimn85l4DlwHPgVsmD55j" -H "Content-Type: application/json" -d '{"reading_meter_number": "9", "meter_number": "745874857", "readingDate": "2025-09-05T00:00:00"}'

curl --insecure -L 'https://auth.smartland.lan/api/v3/oauth2/access_tokens/consumer1/' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer bmZhyTDbsbxU3wufj6vtztMIlEr9fFIUkzfSWGCaimn85l4DlwHPgVsmD55j'