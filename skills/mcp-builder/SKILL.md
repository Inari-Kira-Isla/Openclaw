---
name: scaffold_server
description: MCP Server 骨架生成。當需要快速建立 MCP Server 專案時觸發，包括：專案結構、程式碼模板、依賴配置、測試框架。
---

# Scaffold Server

## 專案結構

```
mcp-server-{name}/
├── src/
│   ├── index.ts          # 入口檔
│   ├── server.ts         # Server 類別
│   └── tools/            # Tool 定義
├── tests/
│   └── server.test.ts
├── package.json
├── tsconfig.json
└── README.md
```

## 核心模板

### Server 類別
```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

class MyServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      { name: 'my-server', version: '1.0.0' },
      { capabilities: { tools: {} } }
    );
    this.setupHandlers();
  }

  private setupHandlers() {
    // Tool handlers
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}
```

## Tool 定義模式

```typescript
const tools = [
  {
    name: 'my_tool',
    description: '工具描述',
    inputSchema: {
      type: 'object',
      properties: {
        param: { type: 'string', description: '參數說明' }
      },
      required: ['param']
    }
  }
];
```

## 建構命令

```bash
# 初始化專案
mkdir mcp-server-myfeature
cd mcp-server-myfeature
npm init -y

# 安裝依賴
npm install @modelcontextprotocol/sdk

# 編譯
npx tsc
```
