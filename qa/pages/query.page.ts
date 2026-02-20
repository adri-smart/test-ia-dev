import { Page, Locator } from '@playwright/test';
import { BasePage } from './base.page';

export class QueryPage extends BasePage {
  readonly queryInput: Locator;
  readonly submitButton: Locator;
  readonly responseArea: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.queryInput = page.locator('[data-testid="query-input"]');
    this.submitButton = page.locator('[data-testid="submit-query-button"]');
    this.responseArea = page.locator('[data-testid="response-area"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async submitQuery(query: string) {
    await this.queryInput.fill(query);
    await this.submitButton.click();
  }

  async getResponseText(): Promise<string> {
    await this.responseArea.waitFor({ state: 'visible', timeout: 10000 });
    return await this.responseArea.textContent() || '';
  }

  async getErrorMessage(): Promise<string> {
    await this.errorMessage.waitFor({ state: 'visible' });
    return await this.errorMessage.textContent() || '';
  }
}
