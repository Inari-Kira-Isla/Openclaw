#!/usr/bin/env node
/**
 * Entity Registry Validator
 * Simple validation functions for entity schemas
 */

const fs = require('fs');
const path = require('path');

const REGISTRY_DIR = path.join(__dirname);

/**
 * Load entity schema by name
 */
function loadSchema(entityName) {
  const registry = JSON.parse(fs.readFileSync(path.join(REGISTRY_DIR, 'registry.json'), 'utf-8'));
  const entity = registry.entities.find(e => e.name === entityName);
  if (!entity) throw new Error(`Entity '${entityName}' not found`);
  return JSON.parse(fs.readFileSync(path.join(REGISTRY_DIR, entity.schema_file), 'utf-8'));
}

/**
 * Validate an entity against its schema
 */
function validate(entityName, data) {
  const schema = loadSchema(entityName);
  return validateAgainstSchema(schema, data);
}

/**
 * Simple schema validation (supports basic types)
 */
function validateAgainstSchema(schema, data, path = '') {
  const errors = [];
  
  // Type check
  if (schema.type && typeof data !== schema.type) {
    errors.push(`${path}: expected ${schema.type}, got ${typeof data}`);
    return { valid: false, errors };
  }
  
  // Required fields
  if (schema.required) {
    for (const field of schema.required) {
      if (!(field in data)) {
        errors.push(`${path}: missing required field '${field}'`);
      }
    }
  }
  
  // Properties validation
  if (schema.properties && typeof data === 'object') {
    for (const [key, propSchema] of Object.entries(schema.properties)) {
      if (key in data) {
        const propPath = path ? `${path}.${key}` : key;
        const propErrors = validateAgainstSchema(propSchema, data[key], propPath);
        errors.push(...propErrors.errors);
      }
    }
  }
  
  // Enum validation
  if (schema.enum && !schema.enum.includes(data)) {
    errors.push(`${path}: value must be one of ${schema.enum.join(', ')}`);
  }
  
  // Array items validation
  if (schema.items && Array.isArray(data)) {
    data.forEach((item, i) => {
      const itemErrors = validateAgainstSchema(schema.items, item, `${path}[${i}]`);
      errors.push(...itemErrors.errors);
    });
  }
  
  return { valid: errors.length === 0, errors };
}

// CLI usage
if (require.main === module) {
  const entity = process.argv[2];
  const inputFile = process.argv[3];
  
  if (!entity || !inputFile) {
    console.log('Usage: validate.js <entity-name> <json-file>');
    console.log('Example: validate.js customer customer-data.json');
    process.exit(1);
  }
  
  try {
    const data = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));
    const result = validate(entity, data);
    
    if (result.valid) {
      console.log('✅ Valid!');
      process.exit(0);
    } else {
      console.log('❌ Invalid:');
      result.errors.forEach(e => console.log(`  - ${e}`));
      process.exit(1);
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { validate, validateAgainstSchema, loadSchema };
