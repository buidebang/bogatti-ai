package com.bogatti.ir.service

import android.content.Context
import org.json.JSONObject
import java.io.File

class ModularConfigManager(private val context: Context) {
    private val configFile = File(context.filesDir, "config.json")
    private var config: JSONObject = JSONObject()

    init {
        loadConfig()
    }

    private fun loadConfig() {
        if (configFile.exists()) {
            config = JSONObject(configFile.readText())
        } else {
            // Initial default config
            config = JSONObject("""
                {
                  "strings": {
                    "app_title": "بوگاتی",
                    "input_placeholder": "اینجا بنویسید..."
                  },
                  "rates": { "toman_per_usd": 100000 },
                  "admin_secret": "secure_key_123"
                }
            """.trimIndent())
            saveConfig()
        }
    }

    fun saveConfig() {
        configFile.writeText(config.toString(2))
    }

    fun setString(key: String, value: String) {
        val strings = config.optJSONObject("strings") ?: JSONObject().also { config.put("strings", it) }
        strings.put(key, value)
        saveConfig()
    }

    fun getString(key: String, default: String = ""): String {
        return config.optJSONObject("strings")?.optString(key, default) ?: default
    }

    fun setTomanRate(rate: Int) {
        val rates = config.optJSONObject("rates") ?: JSONObject().also { config.put("rates", it) }
        rates.put("toman_per_usd", rate)
        saveConfig()
    }

    fun getTomanRate(): Int {
        return config.optJSONObject("rates")?.optInt("toman_per_usd", 100000) ?: 100000
    }

    fun getAdminSecret(): String {
        return config.optString("admin_secret", "secure_key_123")
    }
}
