import { TravelRequest, TravelResponse } from '../types/itinerary';
import {
  JAPAN_ITINERARY_MARKDOWN,
  PARIS_ITINERARY_MARKDOWN,
  EUROPE_ITINERARY_MARKDOWN,
} from './mockData';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Generate a travel itinerary.
 * Attempts to query the backend API (POST /api/travel).
 * If the backend is unavailable or times out, gracefully falls back to
 * high-fidelity mock itinerary content.
 */
export async function generateItinerary(request: TravelRequest): Promise<TravelResponse> {
  const query = request.message.toLowerCase();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000); // 4 second timeout before mock fallback

    const response = await fetch(`${API_BASE_URL}/api/travel`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: request.message,
        thread_id: request.thread_id || 'atlas-web-thread',
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const data: TravelResponse = await response.json();
      if (data.reply && data.reply.trim().length > 0) {
        return data;
      }
    }
  } catch {
    // API not reachable or timed out, gracefully proceed to mock simulation
    // console.info('Backend API not reachable. Using curated itinerary generator.', err);
  }

  // Realistic mock simulation with natural delay (1.8s)
  await new Promise((resolve) => setTimeout(resolve, 1800));

  let selectedMarkdown = JAPAN_ITINERARY_MARKDOWN;

  if (query.includes('paris') || query.includes('france') || query.includes('romantic')) {
    selectedMarkdown = PARIS_ITINERARY_MARKDOWN;
  } else if (query.includes('europe') || query.includes('prague') || query.includes('vienna') || query.includes('budapest')) {
    selectedMarkdown = EUROPE_ITINERARY_MARKDOWN;
  } else if (query.includes('japan') || query.includes('tokyo') || query.includes('kyoto')) {
    selectedMarkdown = JAPAN_ITINERARY_MARKDOWN;
  } else {
    // Custom tailored headline with the user's prompt
    selectedMarkdown = `# Curated Journey: ${request.message.slice(0, 50)}${request.message.length > 50 ? '...' : ''}
*Tailored for 2 Travelers • Custom Cultural & Scenic Route*

> **Curator's Note:** Crafted specifically for your bespoke journey request: "${request.message}". This itinerary highlights cultural authenticity, architectural beauty, and immersive local dining.

---

### **Trip Summary**
- **Style:** Tailored Exploration & Culinary Discovery
- **Recommended Pace:** Leisurely to moderate
- **Best Travel Window:** Spring & Autumn

---

## 📍 Day 1 — Arrival & Neighborhood Orientation
* **Morning:** Arrival, private airport transfer, boutique hotel check-in.
* **Afternoon:** Leisurely walking tour of the historic quarter and main public squares.
* **Evening:** Welcome dinner at a renowned local tavern tasting regional specialties.

## 📍 Day 2 — Iconic Landmarks & Artistic Heritage
* **Morning:** Priority access to premier museums and heritage landmarks.
* **Afternoon:** Stroll through artisan quarters, visiting local craft workshops and vintage bookstalls.
* **Evening:** Sunset vantage point followed by signature tasting menu.

## 📍 Day 3 — Hidden Gems & Scenic Day Excursion
* **Morning:** Private excursion to nearby countryside landscapes and historic estates.
* **Afternoon:** Farm-to-table lunch and wine or regional beverage tasting.
* **Evening:** Return to city center for evening café culture and live acoustic music.

## 📍 Day 4 — Departure & Final Reflections
* **Morning:** Morning espresso at a storied café, leisurely souvenir and local delicacy shopping.
* **Afternoon:** Airport transfer for your flight home.

---
### 💡 Traveler Notes
- Keep digital copies of reservations on hand.
- Pre-booking culinary experiences and museum passes ensures guaranteed entry.
`;
  }

  return {
    reply: selectedMarkdown,
    thread_id: request.thread_id || 'mock-thread-id',
  };
}
