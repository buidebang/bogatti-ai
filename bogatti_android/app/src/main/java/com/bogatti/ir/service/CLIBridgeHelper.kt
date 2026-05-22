package com.bogatti.ir.service

import org.json.JSONObject

/**
 * Utility to format queries for gemini-cli when using SSH tunnels.
 */
object CLIBridgeHelper {

    fun formatForCLI(prompt: String, model: String = "gemini-pro"): String {
        val payload = JSONObject()
        payload.put("model", model)
        payload.put("prompt", prompt)
        payload.put("timestamp", System.currentTimeMillis())

        // Wrap in a base64 string or a specific CLI command pattern
        // Example: gemini-cli --json '{"prompt": "..."}'
        return "gemini-cli --json '${payload.toString().replace("'", "\\'")}'"
    }

    fun parseCLIResponse(rawOutput: String): String {
        return try {
            val json = JSONObject(rawOutput)
            json.optString("response", "No response found in CLI output.")
        } catch (e: Exception) {
            rawOutput // Fallback to raw text if not JSON
        }
    }
}
