# Ubuntu 26.04 Docker 部署

该部署包含三个运行阶段：

- `neo4j`：Neo4j 数据库，数据、日志和插件保存在 Docker 命名卷。
- `app-data-init`：首次部署时将当前 `data/` 和 `logs/` 复制到 Docker 命名卷；已有文件不会被覆盖。
- `ontology-init`：Neo4j 就绪后，从 `src/ontology/wiki_kb/` 幂等加载全部本体和索引。
- `app`：FastAPI、G6 前端、SQL 助手、Chroma 向量库和会话存储。

应用镜像内预缓存了 Chroma 查询所需的多语言 Embedding 模型，因此保留
`HF_HUB_OFFLINE=1` 和 `TRANSFORMERS_OFFLINE=1` 也可离线运行。镜像因此会较大，
首次构建需要下载 Python AI 依赖和模型。

## 1. 安装 Docker

Ubuntu 26.04 可按 Docker 官方仓库安装 Docker Engine 和 Compose 插件。安装完成后确认：

```bash
docker version
docker compose version
```

建议至少准备 4 核 CPU、8 GB 内存和 20 GB 可用磁盘。模型首次加载可能需要额外内存。

## 2. 复制项目和当前文件数据

将整个项目目录复制到服务器，至少包含源码、`.env`、`data/` 和需要保留的 `logs/`。例如：

```bash
rsync -a --exclude .git CamstarSemiOntology/ user@server:/opt/camstar-ontology/
ssh user@server
cd /opt/camstar-ontology
mkdir -p backups data logs
```

`.env` 不进入镜像，但 Compose 会在运行时读取它。确认密码不是示例值：

```bash
grep -E '^(NEO4J_PASSWORD|DEEPSEEK_API_KEY)=' .env
```

容器内应用固定使用 `bolt://neo4j:7687`，所以 `.env` 中原有的 `NEO4J_URI` 不需要手工修改。

## 3. 构建并启动

```bash
docker compose config --quiet
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f ontology-init app
```

部署完成后访问：

- Web：`http://服务器IP:5050`
- 健康检查：`http://服务器IP:5050/healthz`
- Neo4j Browser：默认仅服务器本机可访问 `http://127.0.0.1:7474`

若使用 UFW：

```bash
sudo ufw allow 5050/tcp
```

不要将 7474/7687 直接开放到公网。远程维护可使用 SSH 隧道：

```bash
ssh -L 7474:127.0.0.1:7474 -L 7687:127.0.0.1:7687 user@server
```

## 4. 迁移已有 Neo4j 数据库

默认的 `ontology-init` 会从 JSON 重建项目本体。如果旧库还包含无法由仓库重建的实例数据，应在旧 Neo4j 主机上使用相同主版本的 `neo4j-admin database dump` 导出。

将导出的 `neo4j.dump` 放到新服务器的 `backups/` 后，在首次导入前执行：

```bash
docker compose down
docker compose run --rm --no-deps --user 0 neo4j \
  neo4j-admin database load neo4j \
  --from-path=/backups --overwrite-destination=true
docker compose up -d
```

导入旧数据库后，数据库中的旧认证信息会优先于 `NEO4J_AUTH`；此时应继续使用旧密码，或按 Neo4j 官方流程重置密码。若旧库仅含本体节点，不需要 dump，直接让 `ontology-init` 重建即可。

## 5. 数据位置与备份

查看命名卷：

```bash
docker volume ls --filter name=camstar-ontology
docker compose exec app python -c \
  "from pathlib import Path; print(list(Path('/app/data').iterdir()))"
```

备份 Neo4j 前先停止写入和数据库，然后用一次性容器生成 dump：

```bash
docker compose stop app neo4j
docker compose run --rm --no-deps --user 0 neo4j \
  neo4j-admin database dump neo4j \
  --to-path=/backups --overwrite-destination=true
docker compose up -d
```

应用文件数据可从命名卷导出：

```bash
docker run --rm \
  -v camstar-ontology_app_data:/source:ro \
  -v "$PWD/backups:/backup" \
  alpine tar czf /backup/app-data.tar.gz -C /source .
```

## 6. 更新和日常操作

```bash
# 查看状态和日志
docker compose ps
docker compose logs --tail=200 app neo4j

# 更新源码后重建应用；命名卷不会被删除
docker compose build app ontology-init app-data-init
docker compose up -d

# 手工重新加载本体
docker compose run --rm ontology-init

# 停止但保留数据
docker compose down
```

不要执行 `docker compose down -v`，除非确定要删除全部 Neo4j、Chroma、会话和日志卷。

## 7. 容量调优

默认 Neo4j 配置为 512 MB 初始堆、2 GB 最大堆、1 GB page cache。可在 `.env` 中调整：

```dotenv
NEO4J_HEAP_INITIAL=1g
NEO4J_HEAP_MAX=4g
NEO4J_PAGECACHE=2g
```

修改后执行 `docker compose up -d` 使 Neo4j 重建容器。生产环境建议在 5050 前部署 Nginx/Caddy 和 TLS。
