// ============================================================================
// Knowledge Hub - Google Apps Script Server
// Main server-side logic for the Knowledge Hub system.
// Copy this file into your Google Apps Script editor (Code.gs).
// ============================================================================

// ─── Configuration ───────────────────────────────────
const CONFIG = {
  SHEET_ID: '',              // User fills in their Sheet ID
  TG_BOT_TOKEN: '',          // User fills in Kira bot token
  TG_CHAT_ID: '8399476482',
  USER_EMAIL: '',            // User fills in their email
  REVIEW_HOUR: 9,            // 09:00 PST
  DIGEST_HOUR: 20,           // 20:00 PST
  GMAIL_LABEL: 'knowledge-hub/clip',
};

const TABS = {
  PROJECTS: 'Projects',
  LEARNING: 'Learning',
  INBOX: 'Inbox',
};

const REVIEW_INTERVALS = {
  0: 1,   // Stage 0 -> review after 1 day
  1: 7,   // Stage 1 -> review after 7 days
  2: 30,  // Stage 2 -> review after 30 days
};

const CATEGORIES = ['Tech Insight', 'Error Log', 'Tutorial', 'Concept', 'Tool', 'Pattern'];
const STATUSES = ['Planning', 'Active', 'On Hold', 'Done', 'Cancelled'];
const PRIORITIES = ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low'];


// ============================================================================
// Web App Entry Points
// ============================================================================

/**
 * Serves the web application HTML page.
 * @param {Object} e - The event object from the GET request.
 * @returns {HtmlOutput} The rendered HTML page.
 */
function doGet(e) {
  var template = HtmlService.createTemplateFromFile('WebApp');
  var output = template.evaluate()
    .setTitle('Knowledge Hub')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
  return output;
}

/**
 * Handles API-style POST requests (for future webhook use).
 * @param {Object} e - The event object from the POST request.
 * @returns {TextOutput} JSON response.
 */
function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var action = payload.action || '';
    var result;

    switch (action) {
      case 'addInbox':
        result = addInbox(payload.data);
        break;
      case 'addLearning':
        result = addLearning(payload.data);
        break;
      case 'addProject':
        result = addProject(payload.data);
        break;
      default:
        result = { success: false, error: 'Unknown action: ' + action };
    }

    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: err.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Includes an HTML file's content for use with HtmlService templates.
 * Used inside .html files as: <?!= include('Style') ?>
 * @param {string} filename - The name of the HTML file to include.
 * @returns {string} The raw content of the file.
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}


// ============================================================================
// CRUD Operations — Projects
// ============================================================================

/**
 * Returns all rows from the Projects tab as an array of objects.
 * @returns {Object[]} Array of project objects.
 */
function getProjects() {
  var sheet = _getSheet(TABS.PROJECTS);
  var data = sheet.getDataRange().getValues();
  if (data.length <= 1) return [];

  var headers = data[0];
  var results = [];
  for (var i = 1; i < data.length; i++) {
    var obj = _rowToObject(headers, data[i]);
    if (obj.ProjectId) {
      results.push(obj);
    }
  }
  return results;
}

/**
 * Appends a new project row to the Projects tab with an auto-generated ID.
 * @param {Object} data - The project data (Name, Status, Priority, Description, etc.).
 * @returns {Object} Result with success status and the new project ID.
 */
function addProject(data) {
  var sheet = _getSheet(TABS.PROJECTS);
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var newId = _getNextId(sheet, 'P');
  var today = _formatDate(new Date());

  var obj = {
    ProjectId: newId,
    Name: data.Name || '',
    Status: data.Status || 'Planning',
    Priority: data.Priority || 'P2-Medium',
    Description: data.Description || '',
    Tags: data.Tags || '',
    StartDate: data.StartDate || today,
    EndDate: data.EndDate || '',
    TotalLearningHours: 0,
    Notes: data.Notes || '',
    CreatedAt: today,
    UpdatedAt: today,
  };

  var row = _objectToRow(headers, obj);
  sheet.appendRow(row);

  return { success: true, id: newId };
}

/**
 * Finds a project row by ProjectId and updates the specified fields.
 * @param {string} projectId - The project ID (e.g. "P-001").
 * @param {Object} data - Fields to update.
 * @returns {Object} Result with success status.
 */
function updateProject(projectId, data) {
  var sheet = _getSheet(TABS.PROJECTS);
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var rowNum = _findRowByColumn(sheet, 1, projectId);

  if (rowNum === -1) {
    return { success: false, error: 'Project not found: ' + projectId };
  }

  var existingRow = sheet.getRange(rowNum, 1, 1, headers.length).getValues()[0];
  var existing = _rowToObject(headers, existingRow);

  for (var key in data) {
    if (data.hasOwnProperty(key) && key !== 'ProjectId') {
      existing[key] = data[key];
    }
  }
  existing.UpdatedAt = _formatDate(new Date());

  var newRow = _objectToRow(headers, existing);
  sheet.getRange(rowNum, 1, 1, newRow.length).setValues([newRow]);

  return { success: true, id: projectId };
}


// ============================================================================
// CRUD Operations — Learning
// ============================================================================

/**
 * Returns Learning rows, optionally filtered by category, tags, or projectId.
 * @param {Object} [filters] - Optional filters: { category, tags, projectId }.
 * @returns {Object[]} Array of learning entry objects.
 */
function getLearningEntries(filters) {
  var sheet = _getSheet(TABS.LEARNING);
  var data = sheet.getDataRange().getValues();
  if (data.length <= 1) return [];

  var headers = data[0];
  var results = [];
  filters = filters || {};

  for (var i = 1; i < data.length; i++) {
    var obj = _rowToObject(headers, data[i]);
    if (!obj.LearningId) continue;

    var match = true;

    if (filters.category && obj.Category !== filters.category) {
      match = false;
    }

    if (filters.projectId && obj.ProjectId !== filters.projectId) {
      match = false;
    }

    if (filters.tags) {
      var entryTags = (obj.Tags || '').toLowerCase();
      var searchTag = filters.tags.toLowerCase();
      if (entryTags.indexOf(searchTag) === -1) {
        match = false;
      }
    }

    if (match) {
      results.push(obj);
    }
  }

  return results;
}

/**
 * Appends a new learning entry to the Learning tab.
 * Auto-generates ID (L-NNN) and sets NextReviewDate to tomorrow.
 * @param {Object} data - The learning entry data.
 * @returns {Object} Result with success status and the new learning ID.
 */
function addLearning(data) {
  var sheet = _getSheet(TABS.LEARNING);
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var newId = _getNextId(sheet, 'L');
  var today = _formatDate(new Date());
  var tomorrow = _addDays(today, 1);

  var obj = {
    LearningId: newId,
    Title: data.Title || '',
    Category: data.Category || 'Concept',
    Content: data.Content || '',
    Tags: data.Tags || '',
    ProjectId: data.ProjectId || '',
    SourceURL: data.SourceURL || '',
    HoursSpent: data.HoursSpent || 0,
    ReviewStage: 0,
    NextReviewDate: tomorrow,
    LastReviewedAt: '',
    Confidence: '',
    Notes: data.Notes || '',
    CreatedAt: today,
    UpdatedAt: today,
  };

  var row = _objectToRow(headers, obj);
  sheet.appendRow(row);

  return { success: true, id: newId };
}

/**
 * Updates a specific learning entry by LearningId.
 * @param {string} learningId - The learning ID (e.g. "L-001").
 * @param {Object} data - Fields to update.
 * @returns {Object} Result with success status.
 */
function updateLearning(learningId, data) {
  var sheet = _getSheet(TABS.LEARNING);
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var rowNum = _findRowByColumn(sheet, 1, learningId);

  if (rowNum === -1) {
    return { success: false, error: 'Learning entry not found: ' + learningId };
  }

  var existingRow = sheet.getRange(rowNum, 1, 1, headers.length).getValues()[0];
  var existing = _rowToObject(headers, existingRow);

  for (var key in data) {
    if (data.hasOwnProperty(key) && key !== 'LearningId') {
      existing[key] = data[key];
    }
  }
  existing.UpdatedAt = _formatDate(new Date());

  var newRow = _objectToRow(headers, existing);
  sheet.getRange(rowNum, 1, 1, newRow.length).setValues([newRow]);

  return { success: true, id: learningId };
}

/**
 * Marks a learning entry as reviewed, advances the ReviewStage,
 * calculates the next review date based on spaced repetition intervals,
 * and updates LastReviewedAt.
 * @param {string} learningId - The learning ID.
 * @param {string} confidence - Confidence level after review (e.g. "Low", "Medium", "High").
 * @returns {Object} Result with success status and updated review info.
 */
function markReviewed(learningId, confidence) {
  var sheet = _getSheet(TABS.LEARNING);
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var rowNum = _findRowByColumn(sheet, 1, learningId);

  if (rowNum === -1) {
    return { success: false, error: 'Learning entry not found: ' + learningId };
  }

  var existingRow = sheet.getRange(rowNum, 1, 1, headers.length).getValues()[0];
  var existing = _rowToObject(headers, existingRow);

  var currentStage = parseInt(existing.ReviewStage, 10) || 0;
  var today = _formatDate(new Date());

  // Advance stage if confidence is Medium or High; keep same stage if Low
  var newStage;
  if (confidence === 'Low') {
    newStage = Math.max(0, currentStage - 1);
  } else {
    newStage = Math.min(currentStage + 1, 3);
  }

  // Calculate next review date based on new stage
  var nextReview = '';
  if (newStage < 3) {
    var interval = REVIEW_INTERVALS[newStage] || 30;
    nextReview = _addDays(today, interval);
  }
  // Stage 3 = mastered, no more reviews needed

  existing.ReviewStage = newStage;
  existing.NextReviewDate = nextReview;
  existing.LastReviewedAt = today;
  existing.Confidence = confidence;
  existing.UpdatedAt = today;

  var newRow = _objectToRow(headers, existing);
  sheet.getRange(rowNum, 1, 1, newRow.length).setValues([newRow]);

  return {
    success: true,
    id: learningId,
    newStage: newStage,
    nextReviewDate: nextReview,
    mastered: newStage >= 3,
  };
}


// ============================================================================
// CRUD Operations — Inbox
// ============================================================================

/**
 * Returns all unprocessed Inbox items (Processed != TRUE).
 * @returns {Object[]} Array of inbox item objects.
 */
function getInboxItems() {
  var sheet = _getSheet(TABS.INBOX);
  var data = sheet.getDataRange().getValues();
  if (data.length <= 1) return [];

  var headers = data[0];
  var results = [];

  for (var i = 1; i < data.length; i++) {
    var obj = _rowToObject(headers, data[i]);
    if (!obj.InboxId) continue;

    var processed = String(obj.Processed || '').toUpperCase();
    if (processed !== 'TRUE' && processed !== 'YES') {
      results.push(obj);
    }
  }

  return results;
}

/**
 * Appends a new item to the Inbox tab with an auto-generated ID.
 * @param {Object} data - Inbox item data (Title, Content, Source, etc.).
 * @returns {Object} Result with success status and the new inbox ID.
 */
function addInbox(data) {
  var sheet = _getSheet(TABS.INBOX);
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var newId = _getNextId(sheet, 'I');
  var today = _formatDate(new Date());

  var obj = {
    InboxId: newId,
    Title: data.Title || '',
    Content: data.Content || '',
    Source: data.Source || '',
    SourceURL: data.SourceURL || '',
    Tags: data.Tags || '',
    Processed: 'FALSE',
    MovedTo: '',
    CreatedAt: today,
  };

  var row = _objectToRow(headers, obj);
  sheet.appendRow(row);

  return { success: true, id: newId };
}

/**
 * Marks an Inbox item as processed and records where it was moved.
 * @param {string} inboxId - The inbox item ID (e.g. "I-001").
 * @param {string} moveTo - Where the item was moved (e.g. "Learning", "Projects", "Discarded").
 * @returns {Object} Result with success status.
 */
function processInbox(inboxId, moveTo) {
  var sheet = _getSheet(TABS.INBOX);
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var rowNum = _findRowByColumn(sheet, 1, inboxId);

  if (rowNum === -1) {
    return { success: false, error: 'Inbox item not found: ' + inboxId };
  }

  var existingRow = sheet.getRange(rowNum, 1, 1, headers.length).getValues()[0];
  var existing = _rowToObject(headers, existingRow);

  existing.Processed = 'TRUE';
  existing.MovedTo = moveTo || '';

  var newRow = _objectToRow(headers, existing);
  sheet.getRange(rowNum, 1, 1, newRow.length).setValues([newRow]);

  return { success: true, id: inboxId, movedTo: moveTo };
}


// ============================================================================
// Spaced Repetition Engine
// ============================================================================

/**
 * Main spaced repetition review trigger.
 * Finds all learning entries due for review today (NextReviewDate <= today
 * AND ReviewStage < 3), composes review messages, and sends summaries
 * via Gmail and Telegram.
 */
function runSpacedRepetition() {
  var sheet = _getSheet(TABS.LEARNING);
  var data = sheet.getDataRange().getValues();
  if (data.length <= 1) {
    Logger.log('runSpacedRepetition: No learning entries found.');
    return;
  }

  var headers = data[0];
  var today = _formatDate(new Date());
  var dueItems = [];

  for (var i = 1; i < data.length; i++) {
    var obj = _rowToObject(headers, data[i]);
    if (!obj.LearningId) continue;

    var stage = parseInt(obj.ReviewStage, 10) || 0;
    var nextReview = String(obj.NextReviewDate || '').substring(0, 10);

    if (stage < 3 && nextReview && nextReview <= today) {
      dueItems.push(obj);
    }
  }

  if (dueItems.length === 0) {
    Logger.log('runSpacedRepetition: No items due for review today.');
    return;
  }

  Logger.log('runSpacedRepetition: ' + dueItems.length + ' items due for review.');

  // Build Gmail HTML
  var htmlBody = '<h2>Knowledge Hub - Spaced Repetition Review</h2>';
  htmlBody += '<p><strong>' + dueItems.length + ' item(s) due for review today (' + today + ')</strong></p>';
  htmlBody += '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;font-family:sans-serif;">';
  htmlBody += '<tr style="background:#4a90d9;color:white;">';
  htmlBody += '<th>ID</th><th>Title</th><th>Category</th><th>Stage</th><th>Last Reviewed</th>';
  htmlBody += '</tr>';

  for (var j = 0; j < dueItems.length; j++) {
    var item = dueItems[j];
    var bgColor = j % 2 === 0 ? '#f9f9f9' : '#ffffff';
    htmlBody += '<tr style="background:' + bgColor + ';">';
    htmlBody += '<td>' + item.LearningId + '</td>';
    htmlBody += '<td><strong>' + _escapeHtml(item.Title) + '</strong></td>';
    htmlBody += '<td>' + _escapeHtml(item.Category) + '</td>';
    htmlBody += '<td>' + item.ReviewStage + '/3</td>';
    htmlBody += '<td>' + (item.LastReviewedAt || 'Never') + '</td>';
    htmlBody += '</tr>';
    if (item.Content) {
      htmlBody += '<tr style="background:' + bgColor + ';">';
      htmlBody += '<td colspan="5" style="font-size:0.9em;color:#555;">' + _escapeHtml(String(item.Content).substring(0, 200)) + '</td>';
      htmlBody += '</tr>';
    }
  }
  htmlBody += '</table>';
  htmlBody += '<p style="color:#888;font-size:0.85em;">Open the Knowledge Hub web app to mark items as reviewed.</p>';

  // Send Gmail
  if (CONFIG.USER_EMAIL) {
    GmailApp.sendEmail(CONFIG.USER_EMAIL, 'Knowledge Hub: ' + dueItems.length + ' Review(s) Due', '', {
      htmlBody: htmlBody,
      name: 'Knowledge Hub',
    });
    Logger.log('runSpacedRepetition: Gmail sent to ' + CONFIG.USER_EMAIL);
  }

  // Build Telegram message
  var tgText = '<b>Knowledge Hub Review</b>\n';
  tgText += dueItems.length + ' item(s) due for review today.\n\n';

  var showCount = Math.min(dueItems.length, 5);
  for (var k = 0; k < showCount; k++) {
    var entry = dueItems[k];
    tgText += (k + 1) + '. <b>' + _escapeHtml(entry.Title) + '</b>';
    tgText += ' [' + _escapeHtml(entry.Category) + ', Stage ' + entry.ReviewStage + ']\n';
  }

  if (dueItems.length > 5) {
    tgText += '\n... and ' + (dueItems.length - 5) + ' more.';
  }

  sendTelegram(tgText);
  Logger.log('runSpacedRepetition: Telegram notification sent.');
}


// ============================================================================
// Project Sync
// ============================================================================

/**
 * Iterates the Learning tab, groups entries by ProjectId, sums HoursSpent,
 * and updates the TotalLearningHours column in the Projects tab.
 */
function syncProjectLearningHours() {
  var learningSheet = _getSheet(TABS.LEARNING);
  var learningData = learningSheet.getDataRange().getValues();
  if (learningData.length <= 1) return;

  var learningHeaders = learningData[0];
  var projectIdIdx = learningHeaders.indexOf('ProjectId');
  var hoursIdx = learningHeaders.indexOf('HoursSpent');

  if (projectIdIdx === -1 || hoursIdx === -1) {
    Logger.log('syncProjectLearningHours: ProjectId or HoursSpent column not found in Learning tab.');
    return;
  }

  // Aggregate hours by project
  var hoursMap = {};
  for (var i = 1; i < learningData.length; i++) {
    var pid = String(learningData[i][projectIdIdx] || '').trim();
    if (!pid) continue;

    var hours = parseFloat(learningData[i][hoursIdx]) || 0;
    hoursMap[pid] = (hoursMap[pid] || 0) + hours;
  }

  // Update Projects tab
  var projectSheet = _getSheet(TABS.PROJECTS);
  var projectData = projectSheet.getDataRange().getValues();
  if (projectData.length <= 1) return;

  var projectHeaders = projectData[0];
  var pIdIdx = projectHeaders.indexOf('ProjectId');
  var totalHoursIdx = projectHeaders.indexOf('TotalLearningHours');

  if (pIdIdx === -1 || totalHoursIdx === -1) {
    Logger.log('syncProjectLearningHours: ProjectId or TotalLearningHours column not found in Projects tab.');
    return;
  }

  for (var j = 1; j < projectData.length; j++) {
    var projectId = String(projectData[j][pIdIdx] || '').trim();
    if (!projectId) continue;

    var totalHours = hoursMap[projectId] || 0;
    // Only update if the value has changed
    var currentHours = parseFloat(projectData[j][totalHoursIdx]) || 0;
    if (currentHours !== totalHours) {
      projectSheet.getRange(j + 1, totalHoursIdx + 1).setValue(totalHours);
    }
  }

  Logger.log('syncProjectLearningHours: Synced hours for ' + Object.keys(hoursMap).length + ' projects.');
}


// ============================================================================
// Gmail Web Clipping
// ============================================================================

/**
 * Searches Gmail for emails with the configured label, parses subject and body,
 * appends each to the Inbox tab, and removes the label from processed emails.
 */
function processWebClipEmails() {
  var labelName = CONFIG.GMAIL_LABEL;
  var label = GmailApp.getUserLabelByName(labelName);

  if (!label) {
    Logger.log('processWebClipEmails: Label "' + labelName + '" not found. Creating it.');
    label = GmailApp.createLabel(labelName);
    return;
  }

  var threads = label.getThreads();
  if (threads.length === 0) {
    Logger.log('processWebClipEmails: No threads found with label "' + labelName + '".');
    return;
  }

  var processedCount = 0;

  for (var i = 0; i < threads.length; i++) {
    var messages = threads[i].getMessages();

    for (var j = 0; j < messages.length; j++) {
      var msg = messages[j];
      var subject = msg.getSubject() || '(No Subject)';
      var body = msg.getPlainBody() || '';
      var from = msg.getFrom() || '';

      // Extract first URL from body if present
      var urlMatch = body.match(/https?:\/\/[^\s<>"]+/);
      var sourceUrl = urlMatch ? urlMatch[0] : '';

      // Truncate body to first 2000 chars for the content field
      var content = body.substring(0, 2000).trim();

      addInbox({
        Title: subject,
        Content: content,
        Source: 'Gmail (' + from + ')',
        SourceURL: sourceUrl,
        Tags: 'web-clip',
      });

      processedCount++;
    }

    // Remove the label from the thread after processing
    threads[i].removeLabel(label);
  }

  Logger.log('processWebClipEmails: Processed ' + processedCount + ' email(s) from ' + threads.length + ' thread(s).');
}


// ============================================================================
// Telegram Direct Send
// ============================================================================

/**
 * Sends a message to the configured Telegram chat using the Bot API.
 * @param {string} text - The message text (supports HTML parse_mode).
 * @returns {Object|null} The Telegram API response or null on failure.
 */
function sendTelegram(text) {
  if (!CONFIG.TG_BOT_TOKEN || !CONFIG.TG_CHAT_ID) {
    Logger.log('sendTelegram: Bot token or chat ID not configured.');
    return null;
  }

  var url = 'https://api.telegram.org/bot' + CONFIG.TG_BOT_TOKEN + '/sendMessage';

  var payload = {
    chat_id: CONFIG.TG_CHAT_ID,
    text: text,
    parse_mode: 'HTML',
    disable_web_page_preview: true,
  };

  var options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  };

  try {
    var response = UrlFetchApp.fetch(url, options);
    var result = JSON.parse(response.getContentText());

    if (!result.ok) {
      Logger.log('sendTelegram: API error - ' + result.description);
    }

    return result;
  } catch (err) {
    Logger.log('sendTelegram: Request failed - ' + err.message);
    return null;
  }
}


// ============================================================================
// Daily Digest
// ============================================================================

/**
 * Sends a summary of today's activity via Gmail and Telegram.
 * Includes: new learning entries, updated projects, pending inbox items,
 * and upcoming reviews for tomorrow.
 */
function dailyDigest() {
  var today = _formatDate(new Date());
  var tomorrow = _addDays(today, 1);

  // --- Gather data ---

  // New learning entries added today
  var learningSheet = _getSheet(TABS.LEARNING);
  var learningData = learningSheet.getDataRange().getValues();
  var learningHeaders = learningData.length > 0 ? learningData[0] : [];
  var newLearningToday = [];
  var reviewsTomorrow = [];

  for (var i = 1; i < learningData.length; i++) {
    var lObj = _rowToObject(learningHeaders, learningData[i]);
    if (!lObj.LearningId) continue;

    var createdAt = String(lObj.CreatedAt || '').substring(0, 10);
    if (createdAt === today) {
      newLearningToday.push(lObj);
    }

    var nextReview = String(lObj.NextReviewDate || '').substring(0, 10);
    var stage = parseInt(lObj.ReviewStage, 10) || 0;
    if (nextReview === tomorrow && stage < 3) {
      reviewsTomorrow.push(lObj);
    }
  }

  // Projects updated today
  var projectSheet = _getSheet(TABS.PROJECTS);
  var projectData = projectSheet.getDataRange().getValues();
  var projectHeaders = projectData.length > 0 ? projectData[0] : [];
  var updatedProjectsToday = [];

  for (var j = 1; j < projectData.length; j++) {
    var pObj = _rowToObject(projectHeaders, projectData[j]);
    if (!pObj.ProjectId) continue;

    var pUpdated = String(pObj.UpdatedAt || '').substring(0, 10);
    if (pUpdated === today) {
      updatedProjectsToday.push(pObj);
    }
  }

  // Pending inbox items
  var pendingInbox = getInboxItems();

  // --- Build Gmail HTML ---
  var html = '<h2>Knowledge Hub - Daily Digest (' + today + ')</h2>';

  // New Learning
  html += '<h3>New Learning Entries Today: ' + newLearningToday.length + '</h3>';
  if (newLearningToday.length > 0) {
    html += '<ul>';
    for (var a = 0; a < newLearningToday.length; a++) {
      html += '<li><strong>' + _escapeHtml(newLearningToday[a].Title) + '</strong>';
      html += ' [' + _escapeHtml(newLearningToday[a].Category) + ']</li>';
    }
    html += '</ul>';
  } else {
    html += '<p style="color:#888;">No new entries today.</p>';
  }

  // Updated Projects
  html += '<h3>Projects Updated Today: ' + updatedProjectsToday.length + '</h3>';
  if (updatedProjectsToday.length > 0) {
    html += '<ul>';
    for (var b = 0; b < updatedProjectsToday.length; b++) {
      html += '<li><strong>' + _escapeHtml(updatedProjectsToday[b].Name) + '</strong>';
      html += ' [' + _escapeHtml(updatedProjectsToday[b].Status) + ']</li>';
    }
    html += '</ul>';
  } else {
    html += '<p style="color:#888;">No project updates today.</p>';
  }

  // Pending Inbox
  html += '<h3>Pending Inbox Items: ' + pendingInbox.length + '</h3>';
  if (pendingInbox.length > 0) {
    html += '<ul>';
    var showInbox = Math.min(pendingInbox.length, 10);
    for (var c = 0; c < showInbox; c++) {
      html += '<li>' + _escapeHtml(pendingInbox[c].Title) + '</li>';
    }
    if (pendingInbox.length > 10) {
      html += '<li>... and ' + (pendingInbox.length - 10) + ' more</li>';
    }
    html += '</ul>';
  } else {
    html += '<p style="color:#888;">Inbox clear!</p>';
  }

  // Tomorrow's Reviews
  html += '<h3>Reviews Due Tomorrow: ' + reviewsTomorrow.length + '</h3>';
  if (reviewsTomorrow.length > 0) {
    html += '<ul>';
    for (var d = 0; d < reviewsTomorrow.length; d++) {
      html += '<li><strong>' + _escapeHtml(reviewsTomorrow[d].Title) + '</strong>';
      html += ' [Stage ' + reviewsTomorrow[d].ReviewStage + '/3]</li>';
    }
    html += '</ul>';
  } else {
    html += '<p style="color:#888;">No reviews scheduled for tomorrow.</p>';
  }

  html += '<hr><p style="color:#888;font-size:0.85em;">Knowledge Hub Daily Digest - Auto-generated</p>';

  // Send Gmail
  if (CONFIG.USER_EMAIL) {
    GmailApp.sendEmail(CONFIG.USER_EMAIL, 'Knowledge Hub Digest - ' + today, '', {
      htmlBody: html,
      name: 'Knowledge Hub',
    });
    Logger.log('dailyDigest: Gmail sent.');
  }

  // --- Build Telegram message ---
  var tg = '<b>Knowledge Hub Daily Digest</b>\n';
  tg += today + '\n\n';
  tg += 'New Learning: <b>' + newLearningToday.length + '</b>\n';
  tg += 'Projects Updated: <b>' + updatedProjectsToday.length + '</b>\n';
  tg += 'Inbox Pending: <b>' + pendingInbox.length + '</b>\n';
  tg += 'Reviews Tomorrow: <b>' + reviewsTomorrow.length + '</b>\n';

  if (reviewsTomorrow.length > 0) {
    tg += '\nUpcoming Reviews:\n';
    var showReviews = Math.min(reviewsTomorrow.length, 5);
    for (var e = 0; e < showReviews; e++) {
      tg += '  ' + (e + 1) + '. ' + _escapeHtml(reviewsTomorrow[e].Title) + '\n';
    }
    if (reviewsTomorrow.length > 5) {
      tg += '  ... and ' + (reviewsTomorrow.length - 5) + ' more\n';
    }
  }

  sendTelegram(tg);
  Logger.log('dailyDigest: Telegram sent.');
}


// ============================================================================
// Trigger Setup
// ============================================================================

/**
 * Deletes all existing project triggers and creates the standard set:
 * - runSpacedRepetition: daily at REVIEW_HOUR (09:00 PST)
 * - syncProjectLearningHours: every 6 hours
 * - processWebClipEmails: every 1 hour
 * - dailyDigest: daily at DIGEST_HOUR (20:00 PST)
 *
 * Run this function once from the Apps Script editor to initialize triggers.
 */
function setupTriggers() {
  // Delete all existing triggers for this project
  var existingTriggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < existingTriggers.length; i++) {
    ScriptApp.deleteTrigger(existingTriggers[i]);
  }

  Logger.log('setupTriggers: Deleted ' + existingTriggers.length + ' existing trigger(s).');

  // Spaced repetition review — daily at configured hour
  ScriptApp.newTrigger('runSpacedRepetition')
    .timeBased()
    .atHour(CONFIG.REVIEW_HOUR)
    .everyDays(1)
    .inTimezone('America/Los_Angeles')
    .create();

  // Sync project learning hours — every 6 hours
  ScriptApp.newTrigger('syncProjectLearningHours')
    .timeBased()
    .everyHours(6)
    .create();

  // Process web clip emails — every 1 hour
  ScriptApp.newTrigger('processWebClipEmails')
    .timeBased()
    .everyHours(1)
    .create();

  // Daily digest — daily at configured hour
  ScriptApp.newTrigger('dailyDigest')
    .timeBased()
    .atHour(CONFIG.DIGEST_HOUR)
    .everyDays(1)
    .inTimezone('America/Los_Angeles')
    .create();

  Logger.log('setupTriggers: Created 4 triggers successfully.');
}


// ============================================================================
// File Upload
// ============================================================================

/**
 * Receives file data from the Upload form, saves it to a Drive folder
 * organized as "Knowledge Hub/{ProjectName}", and adds a reference entry
 * to the Learning tab with the Drive file URL.
 * @param {Object} formData - Object with properties: fileName, mimeType, bytes (base64), projectId, projectName, title, category, tags, notes.
 * @returns {Object} Result with success status and file URL.
 */
function uploadFile(formData) {
  try {
    // Get or create the root folder
    var rootFolderName = 'Knowledge Hub';
    var rootFolders = DriveApp.getFoldersByName(rootFolderName);
    var rootFolder;

    if (rootFolders.hasNext()) {
      rootFolder = rootFolders.next();
    } else {
      rootFolder = DriveApp.createFolder(rootFolderName);
    }

    // Get or create the project subfolder
    var projectName = formData.projectName || 'General';
    var subFolders = rootFolder.getFoldersByName(projectName);
    var targetFolder;

    if (subFolders.hasNext()) {
      targetFolder = subFolders.next();
    } else {
      targetFolder = rootFolder.createFolder(projectName);
    }

    // Decode and save the file
    var fileBlob = Utilities.newBlob(
      Utilities.base64Decode(formData.bytes),
      formData.mimeType || 'application/octet-stream',
      formData.fileName || 'uploaded-file'
    );

    var file = targetFolder.createFile(fileBlob);
    var fileUrl = file.getUrl();

    // Add a reference entry to the Learning tab
    addLearning({
      Title: formData.title || formData.fileName || 'Uploaded File',
      Category: formData.category || 'Tool',
      Content: 'File uploaded to Drive: ' + formData.fileName + '\n' + fileUrl,
      Tags: formData.tags || 'file-upload',
      ProjectId: formData.projectId || '',
      SourceURL: fileUrl,
      HoursSpent: 0,
      Notes: formData.notes || '',
    });

    return {
      success: true,
      fileUrl: fileUrl,
      fileName: file.getName(),
      message: 'File uploaded to ' + rootFolderName + '/' + projectName + ' and added to Learning tab.',
    };
  } catch (err) {
    return { success: false, error: 'Upload failed: ' + err.message };
  }
}


// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Gets a sheet by tab name from the configured spreadsheet.
 * @param {string} tabName - The name of the sheet tab.
 * @returns {Sheet} The Google Sheets Sheet object.
 * @throws {Error} If the sheet or tab is not found.
 */
function _getSheet(tabName) {
  var ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
  var sheet = ss.getSheetByName(tabName);

  if (!sheet) {
    throw new Error('Sheet tab "' + tabName + '" not found. Please create it in your spreadsheet.');
  }

  return sheet;
}

/**
 * Scans column A of a sheet for the highest existing ID with the given prefix,
 * and returns the next sequential ID.
 * @param {Sheet} sheet - The Google Sheets Sheet object.
 * @param {string} prefix - The ID prefix (e.g. "P", "L", "I").
 * @returns {string} The next ID (e.g. "P-001", "L-042").
 */
function _getNextId(sheet, prefix) {
  var lastRow = sheet.getLastRow();
  if (lastRow <= 1) {
    return prefix + '-001';
  }

  var ids = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
  var maxNum = 0;

  for (var i = 0; i < ids.length; i++) {
    var id = String(ids[i][0] || '');
    if (id.indexOf(prefix + '-') === 0) {
      var num = parseInt(id.substring(prefix.length + 1), 10);
      if (!isNaN(num) && num > maxNum) {
        maxNum = num;
      }
    }
  }

  var nextNum = maxNum + 1;
  var padded = ('000' + nextNum).slice(-3);
  return prefix + '-' + padded;
}

/**
 * Converts an array row to an object using headers as keys.
 * @param {string[]} headers - Array of column header names.
 * @param {Array} row - Array of cell values.
 * @returns {Object} The row as a key-value object.
 */
function _rowToObject(headers, row) {
  var obj = {};
  for (var i = 0; i < headers.length; i++) {
    var value = (i < row.length) ? row[i] : '';
    // Convert Date objects to formatted strings
    if (value instanceof Date) {
      value = _formatDate(value);
    }
    obj[headers[i]] = (value === null || value === undefined) ? '' : value;
  }
  return obj;
}

/**
 * Converts an object to an array row ordered by headers.
 * @param {string[]} headers - Array of column header names.
 * @param {Object} obj - The data object.
 * @returns {Array} The row as an array of values.
 */
function _objectToRow(headers, obj) {
  var row = [];
  for (var i = 0; i < headers.length; i++) {
    var key = headers[i];
    var value = obj.hasOwnProperty(key) ? obj[key] : '';
    row.push((value === null || value === undefined) ? '' : value);
  }
  return row;
}

/**
 * Finds the row number (1-indexed) where a specific column matches a value.
 * Searches from row 2 onward (skipping header).
 * @param {Sheet} sheet - The Google Sheets Sheet object.
 * @param {number} colIndex - The column index (1-based).
 * @param {string} value - The value to search for.
 * @returns {number} The 1-indexed row number, or -1 if not found.
 */
function _findRowByColumn(sheet, colIndex, value) {
  var lastRow = sheet.getLastRow();
  if (lastRow <= 1) return -1;

  var colData = sheet.getRange(2, colIndex, lastRow - 1, 1).getValues();
  var searchValue = String(value).trim();

  for (var i = 0; i < colData.length; i++) {
    if (String(colData[i][0]).trim() === searchValue) {
      return i + 2; // +2 because data starts at row 2, and array is 0-indexed
    }
  }

  return -1;
}

/**
 * Formats a Date object as a YYYY-MM-DD string.
 * @param {Date} date - The date to format.
 * @returns {string} Formatted date string.
 */
function _formatDate(date) {
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    return '';
  }

  var year = date.getFullYear();
  var month = ('0' + (date.getMonth() + 1)).slice(-2);
  var day = ('0' + date.getDate()).slice(-2);

  return year + '-' + month + '-' + day;
}

/**
 * Adds a specified number of days to a date string and returns the new date string.
 * @param {string} dateStr - The starting date in YYYY-MM-DD format.
 * @param {number} days - Number of days to add (can be negative).
 * @returns {string} The resulting date in YYYY-MM-DD format.
 */
function _addDays(dateStr, days) {
  var parts = String(dateStr).split('-');
  if (parts.length !== 3) return '';

  var date = new Date(
    parseInt(parts[0], 10),
    parseInt(parts[1], 10) - 1,
    parseInt(parts[2], 10)
  );

  date.setDate(date.getDate() + days);

  return _formatDate(date);
}

/**
 * Escapes HTML special characters to prevent injection in HTML output.
 * @param {string} str - The string to escape.
 * @returns {string} The escaped string.
 */
function _escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
