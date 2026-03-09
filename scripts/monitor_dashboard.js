/**
 * 系統監控儀表板
 */

const os = require('os');
const fs = require('fs');
const path = require('path');

function getSystemStatus() {
  const uptime = os.uptime();
  const freeMemory = os.freemem();
  const totalMemory = os.totalmem();
  const cpuLoad = os.loadavg();
  
  return {
    uptime: formatUptime(uptime),
    memory: {
      used: Math.round((totalMemory - freeMemory) / 1024 / 1024 / 1024 * 100) + "%",
      total: Math.round(totalMemory / 1024 / 1024 / 1024) + "GB"
    },
    cpu: {
      load: cpuLoad.map(l => l.toFixed(2)),
      cores: os.cpus().length
    },
    timestamp: new Date().toISOString()
  };
}

function formatUptime(seconds) {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  return `${days}d ${hours}h ${mins}m`;
}

function saveDashboard() {
  const status = getSystemStatus();
  const dashboardPath = path.join(os.homedir(), '.openclaw/logs/dashboard.json');
  
  fs.writeFileSync(dashboardPath, JSON.stringify(status, null, 2));
  console.log("✅ Dashboard updated:", dashboardPath);
  
  return status;
}

if (require.main === module) {
  const status = saveDashboard();
  console.log("\n📊 System Status:");
  console.log(JSON.stringify(status, null, 2));
}

module.exports = { getSystemStatus, saveDashboard };
