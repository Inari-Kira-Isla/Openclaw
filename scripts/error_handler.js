/**
 * 錯誤處理與重試機制
 */

const MAX_RETRIES = 3;
const RETRY_DELAY = 5000;

class ErrorHandler {
  constructor() {
    this.errors = [];
  }
  
  async executeWithRetry(fn, context = "unknown") {
    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
      try {
        return await fn();
      } catch (error) {
        console.error(`Attempt ${attempt}/${MAX_RETRIES} failed:`, error.message);
        if (attempt < MAX_RETRIES) {
          await this.sleep(RETRY_DELAY * attempt);
        } else {
          this.recordError(context, error);
          await this.alert(error, context);
          throw error;
        }
      }
    }
  }
  
  recordError(context, error) {
    this.errors.push({
      context,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
  
  async alert(error, context) {
    // Send alert to Telegram
    const message = `⚠️ Error Alert\nContext: ${context}\nError: ${error.message}`;
    console.log(message);
  }
  
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = new ErrorHandler();
