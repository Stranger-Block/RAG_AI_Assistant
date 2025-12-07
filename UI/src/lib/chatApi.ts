export interface ChatSettings {
  baseUrl: string;
  topK: number;
}

export interface ChatRequest {
  question: string;
  top_k: number;
}

export interface ChatResponse {
  answer: string;
}

const DEFAULT_SETTINGS: ChatSettings = {
  baseUrl: "https://impermeably-pseudostigmatic-nubia.ngrok-free.dev/",
  topK: 3,
};

const STORAGE_KEY = "rag-chatbot-settings";

export function getSettings(): ChatSettings {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return { ...DEFAULT_SETTINGS, ...JSON.parse(stored) };
    }
  } catch (e) {
    console.error("Failed to load settings:", e);
  }
  return DEFAULT_SETTINGS;
}

export function saveSettings(settings: ChatSettings): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch (e) {
    console.error("Failed to save settings:", e);
  }
}

export async function sendMessage(
  question: string,
  settings: ChatSettings
): Promise<string> {
  const url = `${settings.baseUrl}/api/chat`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      top_k: settings.topK,
    } as ChatRequest),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  const data: ChatResponse = await response.json();
  return data.answer;
}
