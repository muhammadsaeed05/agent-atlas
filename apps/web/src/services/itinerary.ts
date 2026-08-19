import { TravelRequest, TravelResponse } from '../types/itinerary';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Generate a travel itinerary by calling the real backend API (POST /api/travel).
 * No mock data fallbacks.
 */
export async function generateItinerary(request: TravelRequest): Promise<TravelResponse> {
  const response = await fetch(`${API_BASE_URL}/api/travel`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: request.message,
      thread_id: request.thread_id || `atlas-web-${Date.now()}`,
    }),
  });

  if (!response.ok) {
    let errorDetail = `Server returned error (${response.status})`;
    try {
      const errData = await response.json();
      if (errData?.detail) {
        errorDetail = typeof errData.detail === 'string' ? errData.detail : JSON.stringify(errData.detail);
      } else if (errData?.message) {
        errorDetail = errData.message;
      }
    } catch {
      // Non-JSON error response body
    }
    throw new Error(errorDetail);
  }

  const data: TravelResponse = await response.json();

  if (!data || !data.reply || data.reply.trim().length === 0) {
    throw new Error('No itinerary was returned by the server. Please try again.');
  }

  return data;
}
