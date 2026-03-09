#!/usr/bin/env node

/**
 * log-action.js - 記錄 Action 到 action.json
 * 用法: node log-action.js <name> <input_json> [output_json]
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.env.HOME, '.openclaw/workspace/learning-engine/action-dataset');
const ACTION_FILE = path.join(DATA_DIR, 'action.json');

function generateId() {
  const count = loadActions().length;
  return `act_${String(count + 1).padStart(3, '0')}`;
}

function loadActions() {
  if (!fs.existsSync(ACTION_FILE)) return [];
  const data = fs.readFileSync(ACTION_FILE, 'utf-8');
  return JSON.parse(data);
}

function saveActions(actions) {
  fs.writeFileSync(ACTION_FILE, JSON.stringify(actions, null, 2));
}

function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('用法: node log-action.js <name> <input_json> [output_json]');
    console.error('範例: node log-action.js "search" \'{"query":"天氣"}\' \'{"result":"晴"}\'');
    process.exit(1);
  }

  const name = args[0];
  const input = JSON.parse(args[1]);
  const output = args[2] ? JSON.parse(args[2]) : {};

  const action = {
    id: generateId(),
    name,
    input,
    output,
    timestamp: new Date().toISOString()
  };

  const actions = loadActions();
  actions.push(action);
  saveActions(actions);

  console.log(`✅ Action 記錄成功: ${action.id}`);
  console.log(JSON.stringify(action, null, 2));
}

main();
