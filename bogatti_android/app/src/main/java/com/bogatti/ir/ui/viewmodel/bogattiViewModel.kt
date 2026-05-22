package com.bogatti.ir.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.bogatti.ir.data.ChatDao
import com.bogatti.ir.data.ChatEntity
import com.bogatti.ir.data.CreditManager
import com.bogatti.ir.service.AIService
import com.bogatti.ir.service.ModularConfigManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class bogattiViewModel(
    private val chatDao: ChatDao,
    private val aiService: AIService,
    private val creditManager: CreditManager,
    private val configManager: ModularConfigManager
) : ViewModel() {

    val chatHistory = chatDao.getAllChats()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _balance = MutableStateFlow(creditManager.getBalanceUsdStr())
    val balance: StateFlow<String> = _balance

    fun getAppTitle() = configManager.getString("app_title", "bogatti")

    fun sendMessage(text: String) {
        val model = configManager.getString("current_model", "gemini-pro")
        val provider = "google"

        viewModelScope.launch {
            chatDao.insertChat(ChatEntity(text = text, sender = "user"))

            val cost = 0.05
            if (creditManager.deductUsd(cost)) {
                _balance.value = creditManager.getBalanceUsdStr()

                _isLoading.value = true
                try {
                    val response = aiService.getResponse(model, provider, text)
                    chatDao.insertChat(ChatEntity(text = response, sender = "ai"))
                } catch (e: Exception) {
                    chatDao.insertChat(ChatEntity(text = "Error: ${e.message}", sender = "ai"))
                } finally {
                    _isLoading.value = false
                }
            } else {
                chatDao.insertChat(ChatEntity(text = "Insufficient balance.", sender = "ai"))
            }
        }
    }

    fun clearHistory() {
        viewModelScope.launch {
            chatDao.clearHistory()
        }
    }
}
