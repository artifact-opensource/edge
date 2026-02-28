#!/usr/bin/env node

/**
 * Copyright Tool - Markdown Front Matter & Banner Manager
 * 
 * Manages copyright information, front matter, and meta banners for markdown files
 * across the entire repository.
 * 
 * Features:
 * - Adds consistent front matter to all markdown files
 * - Injects Artifact Virtual banner (meta-only, non-rendering)
 * - Respects existing front matter and merges intelligently
 * - Backup mechanism for safety
 * - Dry-run mode for preview
 * - Respects .gitignore patterns
 * 
 * Usage:
 *   node copyright-tool.js [options]
 * 
 * Options:
 *   --dry-run, -d        Preview changes without modifying files
 *   --path, -p <path>    Target directory (default: current directory)
 *   --backup, -b         Create backups before modifying (default: true)
 *   --help, -h           Show this help message
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Configuration
const CONFIG = {
  dryRun: process.argv.includes('--dry-run') || process.argv.includes('-d'),
  createBackup: !process.argv.includes('--no-backup'),
  targetPath: getArgValue('--path', '-p') || process.cwd(),
  verbose: process.argv.includes('--verbose') || process.argv.includes('-v'),
  help: process.argv.includes('--help') || process.argv.includes('-h'),
};

// Copyright and organization info
const CURRENT_YEAR = new Date().getFullYear();
const ORG_INFO = {
  name: 'Artifact Virtual (SMC-Private) Limited',
  shortName: 'Artifact Virtual',
  website: 'www.artifactvirtual.com',
  license: 'Proprietary',
  copyrightYear: CURRENT_YEAR,
};

// Artifact Virtual Banner (HTML comment - meta-only, doesn't render)
const ARTIFACT_BANNER = `<!--
╔════════════════════════════════════════════════════════════════════════════╗
║                          ARTIFACT VIRTUAL                                   ║
║                    Enterprise Resource Platform                             ║
║                                                                             ║
║  © ${CURRENT_YEAR} Artifact Virtual (SMC-Private) Limited                     ║
║  All rights reserved. Confidential and Proprietary.                        ║
║                                                                             ║
║  This document is part of the Artifact Virtual Business Infrastructure     ║
║  and contains confidential information. Unauthorized distribution or       ║
║  reproduction is strictly prohibited.                                      ║
╚════════════════════════════════════════════════════════════════════════════╝
-->`;

// Patterns to ignore
const IGNORE_PATTERNS = [
  'node_modules',
  '.git',
  'dist',
  'build',
  'coverage',
  '.next',
  'out',
  'tmp',
];

// Statistics tracking
const stats = {
  filesFound: 0,
  filesProcessed: 0,
  filesModified: 0,
  filesSkipped: 0,
  errors: 0,
};

/**
 * Main execution
 */
async function main() {
  if (CONFIG.help) {
    showHelp();
    process.exit(0);
  }

  console.log('╔════════════════════════════════════════════════════════════════╗');
  console.log('║         Artifact Virtual - Copyright Tool v1.0.0              ║');
  console.log('╚════════════════════════════════════════════════════════════════╝\n');

  if (CONFIG.dryRun) {
    console.log('🔍 DRY RUN MODE - No files will be modified\n');
  }

  console.log(`📂 Target directory: ${CONFIG.targetPath}`);
  console.log(`💾 Backup enabled: ${CONFIG.createBackup}`);
  console.log('');

  // Load project info if available
  loadProjectInfo();

  // Find all markdown files
  console.log('🔎 Discovering markdown files...');
  const markdownFiles = await findMarkdownFiles(CONFIG.targetPath);
  stats.filesFound = markdownFiles.length;
  console.log(`✓ Found ${stats.filesFound} markdown file(s)\n`);

  if (markdownFiles.length === 0) {
    console.log('ℹ️  No markdown files found to process.');
    return;
  }

  // Process each file
  console.log('⚙️  Processing files...\n');
  for (const filePath of markdownFiles) {
    await processMarkdownFile(filePath);
  }

  // Display summary
  displaySummary();
}

/**
 * Load project information from artifact-project.json
 */
function loadProjectInfo() {
  try {
    const projectJsonPath = path.join(CONFIG.targetPath, 'artifact-project.json');
    if (fs.existsSync(projectJsonPath)) {
      const projectData = JSON.parse(fs.readFileSync(projectJsonPath, 'utf8'));
      if (projectData.organization) {
        Object.assign(ORG_INFO, {
          name: projectData.organization.legalName || ORG_INFO.name,
          shortName: projectData.organization.legalName?.split('(')[0].trim() || ORG_INFO.shortName,
          website: projectData.organization.website || ORG_INFO.website,
        });
      }
      if (CONFIG.verbose) {
        console.log('✓ Loaded project information from artifact-project.json');
      }
    }
  } catch (error) {
    if (CONFIG.verbose) {
      console.log('ℹ️  Could not load artifact-project.json, using defaults');
    }
  }
}

/**
 * Find all markdown files recursively
 */
async function findMarkdownFiles(dir) {
  const files = [];
  
  function shouldIgnore(filePath) {
    const relativePath = path.relative(dir, filePath);
    return IGNORE_PATTERNS.some(pattern => 
      relativePath.includes(pattern) || relativePath.startsWith(pattern)
    );
  }

  function walkDir(currentPath) {
    if (shouldIgnore(currentPath)) {
      return;
    }

    try {
      const entries = fs.readdirSync(currentPath, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry.name);
        
        if (shouldIgnore(fullPath)) {
          continue;
        }

        if (entry.isDirectory()) {
          walkDir(fullPath);
        } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.md')) {
          files.push(fullPath);
        }
      }
    } catch (error) {
      if (CONFIG.verbose) {
        console.error(`⚠️  Error reading directory ${currentPath}:`, error.message);
      }
    }
  }

  walkDir(dir);
  return files;
}

/**
 * Process a single markdown file
 */
async function processMarkdownFile(filePath) {
  stats.filesProcessed++;
  
  try {
    const relativePath = path.relative(CONFIG.targetPath, filePath);
    
    // Read file content
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Process the content
    const newContent = addCopyrightAndFrontMatter(content, filePath);
    
    // Check if content changed
    if (content === newContent) {
      stats.filesSkipped++;
      if (CONFIG.verbose) {
        console.log(`  ⏭️  ${relativePath} - No changes needed`);
      }
      return;
    }
    
    // Display changes
    console.log(`  ✏️  ${relativePath}`);
    
    if (CONFIG.dryRun) {
      stats.filesModified++;
      return;
    }
    
    // Create backup if enabled
    if (CONFIG.createBackup) {
      const backupPath = `${filePath}.backup-${Date.now()}`;
      fs.copyFileSync(filePath, backupPath);
      if (CONFIG.verbose) {
        console.log(`     💾 Backup: ${path.basename(backupPath)}`);
      }
    }
    
    // Write modified content
    fs.writeFileSync(filePath, newContent, 'utf8');
    stats.filesModified++;
    
  } catch (error) {
    stats.errors++;
    console.error(`  ❌ Error processing ${filePath}:`, error.message);
  }
}

/**
 * Add copyright banner and front matter to markdown content
 */
function addCopyrightAndFrontMatter(content, filePath) {
  const fileName = path.basename(filePath);
  const relativePath = path.relative(CONFIG.targetPath, filePath);
  
  // Check if file already has our banner
  if (content.includes('ARTIFACT VIRTUAL') && content.includes('Enterprise Resource Platform')) {
    // File already processed, skip
    return content;
  }
  
  // Parse existing front matter if present
  const { frontMatter, body, hasFrontMatter } = parseFrontMatter(content);
  
  // Generate new front matter
  const newFrontMatter = generateFrontMatter(frontMatter, fileName, relativePath);
  
  // Combine banner + front matter + body
  let newContent = ARTIFACT_BANNER + '\n\n';
  
  if (newFrontMatter) {
    newContent += '---\n';
    newContent += newFrontMatter;
    newContent += '---\n\n';
  }
  
  newContent += body.trim() + '\n';
  
  return newContent;
}

/**
 * Parse existing front matter from markdown
 */
function parseFrontMatter(content) {
  const frontMatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
  const match = content.match(frontMatterRegex);
  
  if (match) {
    return {
      frontMatter: parseFrontMatterYAML(match[1]),
      body: match[2],
      hasFrontMatter: true,
    };
  }
  
  return {
    frontMatter: {},
    body: content,
    hasFrontMatter: false,
  };
}

/**
 * Parse YAML-like front matter into object
 */
function parseFrontMatterYAML(yamlText) {
  const result = {};
  const lines = yamlText.split('\n');
  
  for (const line of lines) {
    const match = line.match(/^(\w+):\s*(.+)$/);
    if (match) {
      const key = match[1];
      let value = match[2].trim();
      
      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      
      result[key] = value;
    }
  }
  
  return result;
}

/**
 * Generate front matter for markdown file
 */
function generateFrontMatter(existing, fileName, relativePath) {
  const now = new Date().toISOString();
  
  // Merge with existing, preserving user data
  const frontMatter = {
    title: existing.title || generateTitle(fileName),
    description: existing.description || '',
    author: existing.author || ORG_INFO.shortName,
    copyright: `© ${CURRENT_YEAR} ${ORG_INFO.name}`,
    license: existing.license || ORG_INFO.license,
    classification: existing.classification || 'Confidential',
    lastModified: now,
    documentPath: relativePath,
    artifactVirtual: true,
    ...existing, // Preserve any other custom fields
  };
  
  // Generate YAML
  let yaml = '';
  for (const [key, value] of Object.entries(frontMatter)) {
    if (value !== undefined && value !== null) {
      const escapedValue = String(value).includes(':') || String(value).includes('#') 
        ? `"${value}"` 
        : value;
      yaml += `${key}: ${escapedValue}\n`;
    }
  }
  
  return yaml;
}

/**
 * Generate title from filename
 */
function generateTitle(fileName) {
  return fileName
    .replace('.md', '')
    .replace(/[-_]/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

/**
 * Display summary of operations
 */
function displaySummary() {
  console.log('\n╔════════════════════════════════════════════════════════════════╗');
  console.log('║                        SUMMARY                                 ║');
  console.log('╚════════════════════════════════════════════════════════════════╝\n');
  
  console.log(`  📊 Files found:      ${stats.filesFound}`);
  console.log(`  ⚙️  Files processed:  ${stats.filesProcessed}`);
  console.log(`  ✏️  Files modified:   ${stats.filesModified}`);
  console.log(`  ⏭️  Files skipped:    ${stats.filesSkipped}`);
  console.log(`  ❌ Errors:           ${stats.errors}`);
  
  if (CONFIG.dryRun) {
    console.log('\n  ℹ️  This was a dry run. No files were actually modified.');
    console.log('     Run without --dry-run to apply changes.');
  } else if (stats.filesModified > 0) {
    console.log('\n  ✅ Successfully processed all files!');
    if (CONFIG.createBackup) {
      console.log('     💾 Backups created for modified files.');
    }
  }
  
  console.log('');
}

/**
 * Show help message
 */
function showHelp() {
  console.log(`
Artifact Virtual Copyright Tool
================================

Adds copyright information, front matter, and meta banners to markdown files.

Usage:
  node copyright-tool.js [options]

Options:
  --dry-run, -d         Preview changes without modifying files
  --path, -p <path>     Target directory (default: current directory)
  --no-backup           Don't create backups (backups enabled by default)
  --verbose, -v         Show detailed output
  --help, -h            Show this help message

Examples:
  # Preview changes in current directory
  node copyright-tool.js --dry-run

  # Process specific directory
  node copyright-tool.js --path ./docs

  # Process without creating backups
  node copyright-tool.js --no-backup

  # Verbose dry run
  node copyright-tool.js --dry-run --verbose
  `);
}

/**
 * Get command line argument value
 */
function getArgValue(...flags) {
  for (const flag of flags) {
    const index = process.argv.indexOf(flag);
    if (index !== -1 && index + 1 < process.argv.length) {
      return process.argv[index + 1];
    }
  }
  return null;
}

// Run the tool
if (require.main === module) {
  main().catch(error => {
    console.error('\n❌ Fatal error:', error.message);
    if (CONFIG.verbose) {
      console.error(error.stack);
    }
    process.exit(1);
  });
}

module.exports = { main, findMarkdownFiles, addCopyrightAndFrontMatter };
