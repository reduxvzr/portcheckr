# PortCheckr

## Functionality

- Check given ports
- Writes logs about service availability
- Sends messages to the Telegram bot

## Plans
- Integrate other providers for notifications, such as gotify, rocketchat, default webhooks, etc.
- Multiple ports
- Configuration yaml file for multiple services
- Check for UDP vpn ports, for example, openvpn, wireguard.

## Confuration

Global environmets: 

`NOTIFICATION_TIMEOUT_MINUTES` - timeout between the next try and the port checking failure.

`PORT` - port for service.

`HOST` - host, IP or domain name of server.

`HOST_NAME` - name for host.

`SERVICE_NAME` - name for service, for example, SSH.

`TELEGRAM_BOT_API_TOKEN` - token from BotFather in Telegram.

`TELEGRAM_CHAT_ID`: Chat ID with bot.

## Getting Started

```bash
git clone https://github.com/reduxvzr/portcheckr
cd portcheckr
```

```bash
docker compose up -d --build
```
