export interface TravelRequest {
  message: string;
  thread_id?: string;
}

export interface TravelResponse {
  reply: string;
  thread_id: string;
}

export interface TravelSuggestion {
  id: string;
  label: string;
  prompt: string;
}

export type GenerationStatus = 'idle' | 'loading' | 'success' | 'error';
