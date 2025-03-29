const API_BASE = "http://api.daimonapp.com:8000/api/v1";

export const fetchLLMPapers = async () => {
  try {
    const response = await fetch(`${API_BASE}/papers/?collection_name=LLMPapers`);
    if (!response.ok) throw new Error("Failed to fetch LLM papers");
    return await response.json();
  } catch (error) {
    console.error("API error:", error);
    return [];
  }
};
