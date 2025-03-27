const API_BASE = "http://3.88.199.242:8000/api/v1";

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
