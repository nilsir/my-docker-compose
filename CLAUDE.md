# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此仓库工作时提供指引。

> 沟通和思考请使用中文。生成的所有文档必须为 Markdown 格式，内容使用中文。

## 仓库概述

本仓库是一个 docker-compose 配置集合，每个服务独立放在同名子目录下，可按需单独启动。服务之间通过各自的 external 网络隔离，互不干扰。

## 新增服务的标准步骤

1. 创建服务子目录，例如 `myservice/`
2. 在子目录内添加以下文件：
   - `docker-compose.yml` — 服务定义
   - `.env.example` — 环境变量示例（提交到 git）
   - `.env` — 实际环境变量（不提交到 git）
   - `data/` 目录 — 持久化数据，添加 `.gitkeep` 占位
3. 在根目录 `CLAUDE.md` 的"服务列表"部分追加说明

## 启动任意服务

```bash
# 1. 创建 external 网络（首次运行，每个服务各自的网络名见下方列表）
docker network create <service>-net

# 2. 复制环境变量文件（如 .env 不存在）
cp myservice/.env.example myservice/.env

# 3. 启动
cd myservice && docker compose up -d

# 查看日志
docker compose logs -f

# 停止
docker compose down
```

## docker-compose.yml 编写规范

- 环境变量统一用 `${VAR:-default}` 格式（方便覆盖，同时保留默认值）
- 网络声明 `external: true`，网络名为 `<服务名>-net`
- `container_name` 使用服务名小写
- `restart: unless-stopped`（生产类服务）或 `restart: always`
- 数据持久化挂载到 `./data`，配置文件挂载到 `./conf`（加 `:ro`）

## 各服务网络与默认端口

| 服务            | 网络名            | 默认端口（宿主机）                                          |
|-----------------|-------------------|-------------------------------------------------------------|
| bytebase        | bytebase-net      | 8080                                                        |
| consul          | consul-net        | 8501/8502/8503（UI）                                        |
| elasticsearch   | es-net            | 9200（HTTP）、9300（TCP）、5601（Kibana）                   |
| etcd            | etcd-net          | 2379                                                        |
| jaeger          | jaeger-net        | 16686（UI）、4318（OTLP HTTP）                              |
| mailhog         | mailhog-net       | 1025（SMTP）、8025（UI）                                    |
| meilisearch     | meilisearch-net   | 7700                                                        |
| mongodb         | mongodb-net       | 27017                                                       |
| monitoring      | monitoring-net    | 9090（Prometheus）、3000（Grafana）、9093（Alertmanager）   |
| mysql           | mysql-net         | 3306                                                        |
| mysql8          | mysql8-net        | 3306                                                        |
| neo4j           | neo4j-net         | 7474（HTTP）、7687（Bolt）                                  |
| nginx           | nginx-net         | 8000（HTTP）、443（HTTPS）                                  |
| postgres        | postgres-net      | 5432                                                        |
| rabbitmq        | rabbitmq-net      | 5672、15672（管理 UI）                                      |
| redis           | redis-net         | 6379                                                        |
| sentry          | sentry-net        | 9000                                                        |

## Bytebase

数据库 schema 变更管理平台，支持 MySQL、PostgreSQL、TiDB 等。

```bash
docker network create bytebase-net
cd bytebase && docker compose up -d
# 访问 http://localhost:8080（默认端口，可在 .env 中修改 BYTEBASE_PORT）
```

数据持久化在 `bytebase/data/`，首次访问需完成初始化向导。
