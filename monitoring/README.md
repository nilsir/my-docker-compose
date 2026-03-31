# Monitoring 本地观测套件

Prometheus + Grafana + Alertmanager + 企业微信告警转发，用于采集 vivaia-store 服务的运行指标并在 Grafana 面板中可视化。

---

## 服务一览

| 服务 | 端口 | 说明 |
|------|------|------|
| Prometheus | 9090 | 指标采集，每 15s 抓取一次 `/metrics` |
| Grafana | 3000 | 可视化面板，admin/admin |
| Alertmanager | 9093 | 告警路由，触发后发送企业微信通知 |
| wework-adapter | — (仅内部) | 将 Alertmanager webhook 转换为企业微信群机器人格式 |

---

## 前置条件

- Docker Desktop 已启动
- vivaia-store 服务已在宿主机运行，`/metrics` 端点可访问：

```bash
curl http://localhost:8100/metrics   # vivaia-api
curl http://localhost:8200/metrics   # vivaia-admin
curl http://localhost:8300/metrics   # vivaia-integration
```

---

## 快速启动

### 1. 创建 Docker 外部网络（首次执行一次）

```bash
docker network create monitoring-net
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入企业微信群机器人 webhook key：

```env
WX_WEBHOOK_KEY=your_wechat_robot_key_here   # 从 webhook URL 中的 key= 参数获取
```

> webhook URL 示例：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
> 取 `key=` 后面的值填入即可。

### 3. 启动

```bash
docker-compose up -d
```

首次启动会 build `wework-adapter` 镜像，约需 30s。

### 4. 确认运行状态

```bash
docker-compose ps
```

所有服务应为 `running`。

---

## 访问地址

| 服务 | 地址 | 账号 |
|------|------|------|
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |
| Alertmanager | http://localhost:9093 | — |

---

## 在 Grafana 中查看 metrics 数据

### 步骤一：添加 Prometheus 数据源

1. 打开 http://localhost:3000，用 `admin / admin` 登录
2. 左侧菜单 → **Connections** → **Data sources** → **Add data source**
3. 选择 **Prometheus**
4. URL 填写：`http://prometheus:9090`
5. 点击 **Save & test**，显示 `Successfully queried the Prometheus API` 即成功

### 步骤二：导入 Go 服务面板

1. 左侧菜单 → **Dashboards** → **Import**
2. Dashboard ID 输入 **`14981`**，点击 **Load**
3. 数据源选择刚才添加的 Prometheus
4. 点击 **Import**

面板加载后可看到以下指标：

| 指标 | 说明 |
|------|------|
| `http_requests_total` | 各服务 HTTP 请求总数，按状态码/路由分组 |
| `http_request_duration_seconds` | 请求耗时分布（P50 / P95 / P99） |

---

## 验证 Prometheus 正在抓取 vivaia-store

打开 http://localhost:9090/targets，确认以下三个 job 状态为 **UP**：

- `vivaia-api` → `host.docker.internal:8100`
- `vivaia-admin` → `host.docker.internal:8200`
- `vivaia-integration` → `host.docker.internal:8300`

> 若状态为 DOWN，检查：
> 1. vivaia-store 服务是否已在宿主机运行
> 2. Docker Desktop 是否支持 `host.docker.internal`（macOS/Windows 默认支持）

---

## 告警说明

### 告警规则

规则文件：`prometheus/rules/rules.yml`

| 告警名 | 触发条件 | 级别 |
|--------|---------|------|
| `HighErrorRate` | 5xx 错误率 > 5%，持续 2 分钟 | critical |
| `HighP99Latency` | P99 延迟 > 2s，持续 2 分钟 | warning |

### 企业微信通知

告警触发后经由 `wework-adapter` 转发到企业微信群机器人：

```
Alertmanager → wework-adapter:5000/webhook → 企业微信群机器人
```

`WX_WEBHOOK_KEY` 为空时告警静默（不报错），适合本地开发时暂时关闭通知。

---

## 目录结构

```
monitoring/
├── docker-compose.yml           # 服务编排
├── .env.example                 # 环境变量模板
├── prometheus/
│   ├── prometheus.yml           # 抓取配置（含 vivaia-store 三个服务）
│   └── rules/
│       └── rules.yml            # 告警规则
├── alertmanager/
│   └── alertmanager.yml         # 告警路由配置
└── wework-adapter/
    ├── app.py                   # Flask 转发服务
    └── Dockerfile
```

---

## 停止 / 重启

```bash
# 停止
docker-compose down

# 重启并重新加载配置
docker-compose up -d

# Prometheus 热重载配置（无需重启）
curl -X POST http://localhost:9090/-/reload
```
