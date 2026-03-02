/**
 * 數據自動備份
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BACKUP_DIR = path.join(process.env.HOME, '.openclaw/backups');
const IMPORTANT_FILES = [
  'workspace/TOOLS.md',
  'workspace/AGENTS.md',
  'workspace/SOUL.md',
  'workspace/MEMORY.md',
  'openclaw.json',
  'config/api-keys.yaml'
];

function createBackup() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = path.join(BACKUP_DIR, `backup-${timestamp}`);
  
  // Create backup directory
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }
  
  fs.mkdirSync(backupPath);
  
  let backedUp = 0;
  
  for (const file of IMPORTANT_FILES) {
    const src = path.join(process.env.HOME, '.openclaw', file);
    const dest = path.join(backupPath, file);
    
    if (fs.existsSync(src)) {
      const destDir = path.dirname(dest);
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      fs.copyFileSync(src, dest);
      backedUp++;
      console.log(`✅ Backed up: ${file}`);
    }
  }
  
  console.log(`\n📦 Backup complete: ${backedUp} files backed up to ${backupPath}`);
  
  // Clean old backups (keep last 7)
  cleanupOldBackups();
  
  return { backupPath, backedUp };
}

function cleanupOldBackups() {
  const dirs = fs.readdirSync(BACKUP_DIR)
    .filter(f => f.startsWith('backup-'))
    .sort()
    .reverse();
  
  if (dirs.length > 7) {
    dirs.slice(7).forEach(dir => {
      const fullPath = path.join(BACKUP_DIR, dir);
      execSync(`rm -rf ${fullPath}`);
      console.log(`🗑️ Cleaned old backup: ${dir}`);
    });
  }
}

if (require.main === module) {
  createBackup();
}

module.exports = { createBackup };
