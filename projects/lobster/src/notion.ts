// Notion API Client
import { Client } from '@notionhq/client';
import { LobsterError, SuccessRecord, LobsterConfig, NotionPage } from './types';

export class NotionClient {
  private client: Client;
  private config: LobsterConfig;

  constructor(config: LobsterConfig) {
    this.client = new Client({ auth: config.notionApiKey });
    this.config = config;
  }

  // Create error record
  async createErrorRecord(error: Omit<LobsterError, 'id' | 'createdAt' | 'updatedAt'>): Promise<string> {
    const response = await this.client.pages.create({
      parent: { database_id: this.config.databaseId },
      properties: {
        '類型': {
          select: { name: '錯誤' }
        },
        '來源': {
          select: { name: error.source }
        },
        '嚴重程度': {
          select: { name: error.severity }
        },
        '標題': {
          title: [{ text: { content: error.title } }]
        },
        '描述': {
          rich_text: [{ text: { content: error.description } }]
        },
        '原因': {
          rich_text: error.cause ? [{ text: { content: error.cause } }] : []
        },
        '解決方案': {
          rich_text: error.solution ? [{ text: { content: error.solution } }] : []
        },
        '預防措施': {
          rich_text: error.prevention ? [{ text: { content: error.prevention } }] : []
        },
        '標籤': {
          multi_select: error.tags.map(tag => ({ name: tag }))
        },
        '狀態': {
          select: { name: error.status }
        },
        '發生次數': {
          number: error.occurrenceCount
        }
      }
    });

    return response.id;
  }

  // Create success record
  async createSuccessRecord(success: Omit<SuccessRecord, 'id' | 'createdAt'>): Promise<string> {
    const response = await this.client.pages.create({
      parent: { database_id: this.config.successDatabaseId },
      properties: {
        '類型': {
          select: { name: '成功' }
        },
        '標題': {
          title: [{ text: { content: success.title } }]
        },
        '工作流': {
          rich_text: [{ text: { content: success.workflow } }]
        },
        '描述': {
          rich_text: [{ text: { content: success.description } }]
        },
        '標籤': {
          multi_select: success.tags.map(tag => ({ name: tag }))
        },
        ' lessons': {
          rich_text: success.lessons.map(lesson => ({ text: { content: lesson } }))
        }
      }
    });

    return response.id;
  }

  // Search errors by keyword
  async searchErrors(keyword: string): Promise<NotionPage[]> {
    const response = await this.client.databases.query({
      database_id: this.config.databaseId,
      filter: {
        and: [
          {
            property: '類型',
            select: { equals: '錯誤' }
          },
          {
            or: [
              {
                property: '標題',
                title: { contains: keyword }
              },
              {
                property: '描述',
                rich_text: { contains: keyword }
              }
            ]
          }
        ]
      }
    });

    return response.results as NotionPage[];
  }

  // Get all open errors
  async getOpenErrors(): Promise<NotionPage[]> {
    const response = await this.client.databases.query({
      database_id: this.config.databaseId,
      filter: {
        and: [
          {
            property: '類型',
            select: { equals: '錯誤' }
          },
          {
            property: '狀態',
            select: { does_not_equal: 'Resolved' }
          }
        ]
      }
    });

    return response.results as NotionPage[];
  }

  // Update error status
  async updateErrorStatus(pageId: string, status: string): Promise<void> {
    await this.client.pages.update({
      page_id: pageId,
      properties: {
        '狀態': {
          select: { name: status }
        }
      }
    });
  }

  // Get error statistics
  async getErrorStats(): Promise<{ total: number; open: number; resolved: number; bySeverity: Record<string, number> }> {
    const allErrors = await this.client.databases.query({
      database_id: this.config.databaseId,
      filter: {
        property: '類型',
        select: { equals: '錯誤' }
      }
    });

    const pages = allErrors.results as NotionPage[];
    let open = 0;
    let resolved = 0;
    const bySeverity: Record<string, number> = { high: 0, medium: 0, low: 0 };

    for (const page of pages) {
      const statusProp = page.properties['狀態'] as { select?: { name: string } };
      const severityProp = page.properties['嚴重程度'] as { select?: { name: string } };

      if (statusProp?.select?.name === 'Resolved') resolved++;
      else open++;

      const severity = severityProp?.select?.name?.toLowerCase();
      if (severity && bySeverity[severity] !== undefined) {
        bySeverity[severity]++;
      }
    }

    return { total: pages.length, open, resolved, bySeverity };
  }
}
