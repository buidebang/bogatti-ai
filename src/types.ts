export type Role = 'user' | 'assistant';

export interface Message {
  id: string;
  role: Role;
  content: string;
}

export interface ModelProvider {
  id: string;
  name: string;
  creditCost: number;
}

export const MODELS: ModelProvider[] = [
  { id: 'gemini-3.1-pro-preview', name: 'Gemini 3.1', creditCost: 2 },
  { id: 'gpt-5.4-placeholder', name: 'GPT-5.4 (Placeholder)', creditCost: 5 }
];
