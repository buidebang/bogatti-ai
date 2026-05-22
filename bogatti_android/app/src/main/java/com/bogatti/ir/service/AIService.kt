package com.bogatti.ir.service

import kotlinx.coroutines.delay
import android.util.Log

class AIService(private val useSSHBridge: Boolean = false) {

    suspend fun getResponse(modelName: String, provider: String, prompt: String, systemPrompt: String? = null): String {
        // Simulation of API call with delay
        delay(1500)

        if (useSSHBridge) {
            val cliCommand = CLIBridgeHelper.formatForCLI(prompt, modelName)
            Log.d("bogattiAI", "Executing via SSH/CLI Bridge: $cliCommand")
            // In a real implementation, this would execute the command over SSH
            // and return the parsed result.
            return "bogatti (SSH Bridge): ${prompt.reversed()} (Simulated response for low-bandwidth)"
        }

        return when (provider.lowercase()) {
            "openai" -> "OpenAI ($modelName): سلام کاربر عزیز. درخواست شما در bogatti AI پردازش شد."
            "google" -> "Google ($modelName): من با تمام توان در خدمت شما هستم."
            "anthropic" -> "Anthropic ($modelName): خوشحالم که می‌توانم به سوالات شما پاسخ دهم."
            else -> "مدل یا سرویس‌دهنده پشتیبانی نمی‌شود."
        }
    }
}
