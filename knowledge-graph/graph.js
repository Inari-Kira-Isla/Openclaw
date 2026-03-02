#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const GRAPH_FILE = path.join(__dirname, 'data', 'graph.json');

// 初始化圖譜
function initGraph() {
  if (!fs.existsSync(GRAPH_FILE)) {
    fs.writeFileSync(GRAPH_FILE, JSON.stringify({ nodes: [], edges: [] }, null, 2));
  }
}

// 新增節點
function addNode(type, label, properties = {}) {
  initGraph();
  const graph = JSON.parse(fs.readFileSync(GRAPH_FILE, 'utf8'));
  
  const node = {
    id: `node_${Date.now()}`,
    type,
    label,
    properties,
    created_at: new Date().toISOString()
  };
  
  graph.nodes.push(node);
  fs.writeFileSync(GRAPH_FILE, JSON.stringify(graph, null, 2));
  console.log('✅ 新增節點:', node.id, label);
  return node;
}

// 列出節點
function listNodes(type = null) {
  initGraph();
  const graph = JSON.parse(fs.readFileSync(GRAPH_FILE, 'utf8'));
  const nodes = type ? graph.nodes.filter(n => n.type === type) : graph.nodes;
  console.log(`📊 節點總數: ${nodes.length}`);
  nodes.forEach(n => console.log(`  - ${n.id}: ${n.label} (${n.type})`));
}

// 新增邊
function addEdge(source, target, relation, weight = 1.0) {
  initGraph();
  const graph = JSON.parse(fs.readFileSync(GRAPH_FILE, 'utf8'));
  
  // 驗證節點存在
  if (!graph.nodes.find(n => n.id === source)) throw new Error('Source node not found');
  if (!graph.nodes.find(n => n.id === target)) throw new Error('Target node not found');
  
  const edge = {
    id: `edge_${Date.now()}`,
    source,
    target,
    relation,
    weight,
    created_at: new Date().toISOString()
  };
  
  graph.edges.push(edge);
  fs.writeFileSync(GRAPH_FILE, JSON.stringify(graph, null, 2));
  console.log('✅ 新增邊:', source, '→', target, `(${relation})`);
  return edge;
}

// 查詢路徑（簡單版：BFS）
function findPath(start, end, maxDepth = 3) {
  initGraph();
  const graph = JSON.parse(fs.readFileSync(GRAPH_FILE, 'utf8'));
  
  const queue = [[start]];
  const visited = new Set([start]);
  
  while (queue.length > 0) {
    const path = queue.shift();
    const current = path[path.length - 1];
    
    if (current === end) {
      return path;
    }
    
    if (path.length >= maxDepth) continue;
    
    const neighbors = graph.edges
      .filter(e => e.source === current)
      .map(e => e.target);
    
    for (const neighbor of neighbors) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push([...path, neighbor]);
      }
    }
  }
  
  return null;
}

// CLI
const args = process.argv.slice(2);
try {
  if (args[0] === 'add-node' && args[1] && args[2]) {
    addNode(args[1], args[2], {});
  } else if (args[0] === 'list-nodes') {
    listNodes(args[1]);
  } else if (args[0] === 'add-edge' && args[1] && args[2] && args[3]) {
    addEdge(args[1], args[2], args[3]);
  } else if (args[0] === 'path' && args[1] && args[2]) {
    const p = findPath(args[1], args[2]);
    console.log(p ? `路徑: ${p.join(' → ')}` : '未找到路徑');
  } else {
    console.log('用法:');
    console.log('  node graph.js add-node <type> <label>');
    console.log('  node graph.js list-nodes [type]');
    console.log('  node graph.js add-edge <source> <target> <relation>');
    console.log('  node graph.js path <start> <end>');
  }
} catch (e) {
  console.error('❌ Error:', e.message);
}
