/**
 * Event Contract Validator for Muse Core
 * Validates events against base-event schema and registry
 */

const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const fs = require('fs');
const path = require('path');

// Load schemas
const baseEventSchema = require('./base-event.json');
const eventsRegistry = require('./events-registry.json');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);
const validateBaseEvent = ajv.compile(baseEventSchema);

/**
 * Validate an event against the base event schema
 * @param {Object} event - Event object to validate
 * @returns {{ valid: boolean, errors?: Array }}
 */
function validateEvent(event) {
  const valid = validateBaseEvent(event);
  
  if (!valid) {
    return {
      valid: false,
      errors: validateBaseEvent.errors
    };
  }
  
  return { valid: true };
}

/**
 * Check if an event type is registered
 * @param {string} type - Event type to check
 * @returns {boolean}
 */
function isEventTypeRegistered(type) {
  return eventsRegistry.registeredEvents.includes(type);
}

/**
 * Validate event type and category
 * @param {Object} event - Event object
 * @returns {{ valid: boolean, error?: string }}
 */
function validateEventType(event) {
  if (!event.type) {
    return { valid: false, error: 'Missing event type' };
  }
  
  if (!isEventTypeRegistered(event.type)) {
    return { valid: false, error: `Unregistered event type: ${event.type}` };
  }
  
  if (event.category && !baseEventSchema.properties.category.enum.includes(event.category)) {
    return { valid: false, error: `Invalid category: ${event.category}` };
  }
  
  return { valid: true };
}

/**
 * Full validation: schema + registry
 * @param {Object} event - Event to validate
 * @returns {{ valid: boolean, errors?: Array, error?: string }}
 */
function validateFull(event) {
  // Schema validation
  const schemaResult = validateEvent(event);
  if (!schemaResult.valid) {
    return schemaResult;
  }
  
  // Registry validation
  const typeResult = validateEventType(event);
  if (!typeResult.valid) {
    return typeResult;
  }
  
  return { valid: true };
}

/**
 * Create a new event with defaults
 * @param {string} type - Event type
 * @param {Object} payload - Event payload
 * @param {string} source - Event source
 * @param {string} category - Event category
 * @returns {Object}
 */
function createEvent(type, payload, source, category) {
  const traceId = `trace-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  
  return {
    type,
    payload,
    timestamp: new Date().toISOString(),
    source,
    version: '1.0.0',
    traceId,
    category
  };
}

module.exports = {
  validateEvent,
  validateEventType,
  validateFull,
  isEventTypeRegistered,
  createEvent,
  baseEventSchema,
  eventsRegistry
};

// CLI test
if (require.main === module) {
  const testEvent = createEvent(
    'knowledge.memory.stored',
    { key: 'test-key', size: 1024 },
    'muse-core',
    'knowledge-update'
  );
  
  console.log('Test Event:', JSON.stringify(testEvent, null, 2));
  console.log('Validation:', validateFull(testEvent));
}
