# Sentry

Self-hosted Sentry 错误追踪服务。

## 使用方法

### 1. 创建网络

```bash
docker network create sentry-net
```

### 2. 复制环境变量配置

```bash
cp .env.example .env
```

修改 `.env` 中的配置，特别是 `SENTRY_SECRET_KEY`。

生成 secret key:
```bash
docker run --rm --platform linux/amd64 getsentry/sentry config generate-secret-key
```

### 3. 初始化数据库

首次启动前需要初始化数据库和创建管理员用户：

```bash
docker-compose run --rm sentry upgrade
```

按照提示创建管理员账户。

### 4. 启动服务

```bash
docker-compose up -d
```

### 5. 访问

浏览器访问: http://localhost:9000

## 端口

| 服务 | 端口 |
|------|------|
| Sentry Web | 9000 |

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| SENTRY_PORT | 9000 | Web 服务端口 |
| SENTRY_SECRET_KEY | - | 必须设置的密钥 |
| SENTRY_DB_USER | sentry | 数据库用户名 |
| SENTRY_DB_PASSWORD | sentry | 数据库密码 |
| SENTRY_DB_NAME | sentry | 数据库名称 |
