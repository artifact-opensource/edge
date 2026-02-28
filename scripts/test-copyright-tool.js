#!/usr/bin/env node

/**
 * Test Suite for Copyright Tool
 * 
 * Comprehensive end-to-end tests for the copyright tool
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const TEST_DIR = '/tmp/copyright_tool_test';
const SCRIPT_PATH = path.join(__dirname, 'copyright-tool.js');

// Test results tracking
let testsRun = 0;
let testsPassed = 0;
let testsFailed = 0;

/**
 * Test utility functions
 */
function assert(condition, message) {
  testsRun++;
  if (condition) {
    testsPassed++;
    console.log(`  ✅ ${message}`);
  } else {
    testsFailed++;
    console.log(`  ❌ ${message}`);
  }
}

function runTest(name, testFn) {
  console.log(`\n🧪 Running: ${name}`);
  try {
    testFn();
  } catch (error) {
    testsFailed++;
    console.log(`  ❌ Test failed with error: ${error.message}`);
  }
}

function setupTestEnv() {
  // Clean and create test directory
  if (fs.existsSync(TEST_DIR)) {
    fs.rmSync(TEST_DIR, { recursive: true, force: true });
  }
  fs.mkdirSync(TEST_DIR, { recursive: true });
}

function cleanupTestEnv() {
  if (fs.existsSync(TEST_DIR)) {
    fs.rmSync(TEST_DIR, { recursive: true, force: true });
  }
}

function createTestFile(relativePath, content) {
  const fullPath = path.join(TEST_DIR, relativePath);
  const dir = path.dirname(fullPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(fullPath, content, 'utf8');
  return fullPath;
}

function runCopyrightTool(args = '') {
  const cmd = `node ${SCRIPT_PATH} --path ${TEST_DIR} ${args}`;
  try {
    const output = execSync(cmd, { encoding: 'utf8' });
    return output;
  } catch (error) {
    throw new Error(`Tool execution failed: ${error.message}`);
  }
}

/**
 * Test 1: File Discovery
 */
runTest('File Discovery - Finds all markdown files', () => {
  setupTestEnv();
  
  createTestFile('test1.md', '# Test 1');
  createTestFile('sub/test2.md', '# Test 2');
  createTestFile('sub/deep/test3.md', '# Test 3');
  
  const output = runCopyrightTool('--dry-run');
  
  assert(output.includes('Found 3 markdown file'), 'Should find 3 markdown files');
  assert(output.includes('test1.md'), 'Should find test1.md');
  assert(output.includes('test2.md'), 'Should find test2.md');
  assert(output.includes('test3.md'), 'Should find test3.md');
  
  cleanupTestEnv();
});

/**
 * Test 2: Banner Injection
 */
runTest('Banner Injection - Adds Artifact Virtual banner', () => {
  setupTestEnv();
  
  createTestFile('test.md', '# Original Content');
  runCopyrightTool();
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  
  assert(content.includes('ARTIFACT VIRTUAL'), 'Should contain banner header');
  assert(content.includes('Enterprise Resource Platform'), 'Should contain platform name');
  assert(content.includes('©'), 'Should contain copyright symbol');
  assert(content.includes('Artifact Virtual (SMC-Private) Limited'), 'Should contain company name');
  assert(content.startsWith('<!--'), 'Banner should be in HTML comment');
  
  cleanupTestEnv();
});

/**
 * Test 3: Front Matter Addition
 */
runTest('Front Matter Addition - Adds YAML front matter', () => {
  setupTestEnv();
  
  createTestFile('test.md', '# Test Content');
  runCopyrightTool();
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  
  assert(content.includes('---'), 'Should have YAML delimiters');
  assert(content.includes('title:'), 'Should have title field');
  assert(content.includes('copyright:'), 'Should have copyright field');
  assert(content.includes('license:'), 'Should have license field');
  assert(content.includes('classification:'), 'Should have classification field');
  assert(content.includes('lastModified:'), 'Should have lastModified field');
  assert(content.includes('documentPath:'), 'Should have documentPath field');
  assert(content.includes('artifactVirtual: true'), 'Should mark as artifactVirtual');
  
  cleanupTestEnv();
});

/**
 * Test 4: Preserve Existing Front Matter
 */
runTest('Front Matter Preservation - Merges with existing', () => {
  setupTestEnv();
  
  const originalContent = `---
title: Custom Title
author: John Doe
custom_field: custom_value
---

# Content`;
  
  createTestFile('test.md', originalContent);
  runCopyrightTool();
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  
  assert(content.includes('title: Custom Title'), 'Should preserve custom title');
  assert(content.includes('author: John Doe'), 'Should preserve custom author');
  assert(content.includes('custom_field: custom_value'), 'Should preserve custom fields');
  assert(content.includes('copyright:'), 'Should add copyright field');
  
  cleanupTestEnv();
});

/**
 * Test 5: Idempotency
 */
runTest('Idempotency - Running twice does not duplicate', () => {
  setupTestEnv();
  
  createTestFile('test.md', '# Test');
  
  // First run
  runCopyrightTool();
  const firstContent = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  
  // Second run
  const output = runCopyrightTool('--verbose');
  const secondContent = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  
  assert(firstContent === secondContent, 'Content should be identical after second run');
  assert(output.includes('No changes needed'), 'Should skip already processed files');
  
  cleanupTestEnv();
});

/**
 * Test 6: Backup Creation
 */
runTest('Backup Creation - Creates backups before modification', () => {
  setupTestEnv();
  
  createTestFile('test.md', '# Original');
  runCopyrightTool();
  
  const backupFiles = fs.readdirSync(TEST_DIR).filter(f => f.includes('.backup-'));
  
  assert(backupFiles.length > 0, 'Should create backup files');
  
  const backupContent = fs.readFileSync(path.join(TEST_DIR, backupFiles[0]), 'utf8');
  assert(backupContent === '# Original', 'Backup should contain original content');
  
  cleanupTestEnv();
});

/**
 * Test 7: Dry Run Mode
 */
runTest('Dry Run Mode - Does not modify files', () => {
  setupTestEnv();
  
  const originalContent = '# Test Content';
  createTestFile('test.md', originalContent);
  
  runCopyrightTool('--dry-run');
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  
  assert(content === originalContent, 'Content should remain unchanged in dry-run');
  
  const backupFiles = fs.readdirSync(TEST_DIR).filter(f => f.includes('.backup-'));
  assert(backupFiles.length === 0, 'Should not create backups in dry-run');
  
  cleanupTestEnv();
});

/**
 * Test 8: No Backup Mode
 */
runTest('No Backup Mode - Skips backup creation', () => {
  setupTestEnv();
  
  createTestFile('test.md', '# Test');
  runCopyrightTool('--no-backup');
  
  const backupFiles = fs.readdirSync(TEST_DIR).filter(f => f.includes('.backup-'));
  
  assert(backupFiles.length === 0, 'Should not create backups with --no-backup');
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  assert(content.includes('ARTIFACT VIRTUAL'), 'Should still modify files');
  
  cleanupTestEnv();
});

/**
 * Test 9: Directory Ignore Patterns
 */
runTest('Ignore Patterns - Respects node_modules and other patterns', () => {
  setupTestEnv();
  
  createTestFile('test.md', '# Valid file');
  createTestFile('node_modules/package.md', '# Should be ignored');
  createTestFile('.git/info.md', '# Should be ignored');
  createTestFile('dist/build.md', '# Should be ignored');
  
  const output = runCopyrightTool('--dry-run');
  
  assert(output.includes('Found 1 markdown file'), 'Should only find 1 valid file');
  assert(!output.includes('node_modules'), 'Should ignore node_modules');
  assert(!output.includes('.git'), 'Should ignore .git');
  assert(!output.includes('dist'), 'Should ignore dist');
  
  cleanupTestEnv();
});

/**
 * Test 10: Title Generation
 */
runTest('Title Generation - Creates title from filename', () => {
  setupTestEnv();
  
  createTestFile('api-documentation.md', '# Content');
  runCopyrightTool();
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'api-documentation.md'), 'utf8');
  
  assert(content.includes('title: Api Documentation'), 'Should generate title from filename');
  
  cleanupTestEnv();
});

/**
 * Test 11: Deep Nesting
 */
runTest('Deep Nesting - Handles deeply nested files', () => {
  setupTestEnv();
  
  createTestFile('a/b/c/d/e/f/deep.md', '# Deep file');
  runCopyrightTool();
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'a/b/c/d/e/f/deep.md'), 'utf8');
  
  assert(content.includes('documentPath: a/b/c/d/e/f/deep.md'), 'Should track correct path');
  assert(content.includes('ARTIFACT VIRTUAL'), 'Should process deep files');
  
  cleanupTestEnv();
});

/**
 * Test 12: HTML Comment Format
 */
runTest('HTML Comment Format - Banner is in comment', () => {
  setupTestEnv();
  
  createTestFile('test.md', '# Test');
  runCopyrightTool();
  
  const content = fs.readFileSync(path.join(TEST_DIR, 'test.md'), 'utf8');
  const lines = content.split('\n');
  
  assert(lines[0] === '<!--', 'Should start with HTML comment opening');
  const closingIndex = lines.findIndex(l => l === '-->');
  assert(closingIndex > 0, 'Should have HTML comment closing');
  
  cleanupTestEnv();
});

/**
 * Display Test Summary
 */
console.log('\n╔════════════════════════════════════════════════════════════════╗');
console.log('║                    TEST SUMMARY                                ║');
console.log('╚════════════════════════════════════════════════════════════════╝\n');

console.log(`  Total tests run:     ${testsRun}`);
console.log(`  Tests passed:        ${testsPassed} ✅`);
console.log(`  Tests failed:        ${testsFailed} ❌`);
console.log(`  Success rate:        ${Math.round((testsPassed / testsRun) * 100)}%`);
console.log('');

if (testsFailed === 0) {
  console.log('✅ All tests passed!\n');
  process.exit(0);
} else {
  console.log('❌ Some tests failed!\n');
  process.exit(1);
}
