# PostgreSQL Configuration for Orb

## 优化说明

此配置已针对 Orb 应用进行优化,包含以下改进:

### 1. 性能优化
- `shared_buffers = 256MB` - 共享内存缓冲区
- `effective_cache_size = 1GB` - 可用缓存大小
- `work_mem = 16MB` - 每个查询操作的内存
- `maintenance_work_mem = 64MB` - 维护操作内存

### 2. 连接配置
- `max_connections = 200` - 支持最多 200 个并发连接
- 添加了健康检查确保服务可用性

### 3. WAL 配置
- 优化了 Write-Ahead Logging 设置以提高写入性能
- `wal_level = replica` - 支持复制

### 4. 镜像配置
- 使用最新的 `postgres` 镜像 (当前为 PostgreSQL 18+)
- PostgreSQL 18+ 使用新的数据目录结构,挂载到 `/var/lib/postgresql`

## 使用方法

1. 确保网络已创建:
```bash
docker network create postgres-net
```

2. 启动服务:
```bash
cd /Users/alante/code/docker/my-docker-compose/postgres
docker-compose up -d
```

3. 查看日志:
```bash
docker-compose logs -f postgres
```

4. 验证配置:
```bash
docker exec -it postgres psql -U nilsir -c "SHOW shared_buffers;"
docker exec -it postgres psql -U nilsir -c "SHOW max_connections;"
```

5. 连接数据库:
```bash
docker exec -it postgres psql -U nilsir -d nilsir
```

## 目录结构

```
postgres/
├── docker-compose.yml       # Docker Compose 配置
├── postgresql.conf          # PostgreSQL 优化配置
├── .env                     # 环境变量配置
└── data/                    # 数据持久化目录 (自动创建)
    └── 18/                  # PostgreSQL 18+ 版本数据
```

## 注意事项

- PostgreSQL 18+ 数据存储在 `./data/18/docker/` 目录下
- 如果遇到内存不足,可以降低 `postgresql.conf` 中的 `shared_buffers` 和 `effective_cache_size`
- 自定义配置文件位于 `./postgresql.conf`
- 数据持久化在 `./data` 目录,需要添加到 `.gitignore`
- 环境变量可通过 `.env` 文件自定义

## 环境变量

在 `.env` 文件中可配置:

```bash
POSTGRES_USER=nilsir          # 数据库用户名
POSTGRES_PASSWORD=nilsir      # 数据库密码
POSTGRES_DB=nilsir            # 默认数据库名
POSTGRES_PORT=5432            # 暴露端口
```

## 备份与恢复

### 备份数据库
```bash
docker exec postgres pg_dump -U nilsir nilsir > backup.sql
```

### 恢复数据库
```bash
docker exec -i postgres psql -U nilsir nilsir < backup.sql
```

## 故障排查

### 查看容器状态
```bash
docker-compose ps
```

### 查看实时日志
```bash
docker-compose logs -f postgres
```

### 检查数据库连接
```bash
docker exec postgres pg_isready -U nilsir
```

### 重启服务
```bash
docker-compose restart postgres
```

### 完全重建（会清除数据）
```bash
docker-compose down
rm -rf data
docker-compose up -d
```
