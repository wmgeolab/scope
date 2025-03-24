/**
 * API helper class for constructing URLs and making API calls
 */
export class API {
  /**
   * Constructs a complete API URL by combining the base URL with an optional path
   * @param {string} [path] - Optional path to append to the base URL
   * @returns {string} The complete API URL
   */
  static url(path = '') {
    const baseURL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
    return path ? `${baseURL}${path}` : baseURL;
  }

  /**
   * Gets the authentication headers for API requests
   * @returns {Object} Headers object with authentication token
   */
  static getAuthHeaders() {
    return {
      "Content-Type": "application/json",
      Authorization: "Token " + localStorage.getItem("user"),
    };
  }
} 