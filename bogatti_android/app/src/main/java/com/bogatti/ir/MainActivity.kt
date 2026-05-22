package com.bogatti.ir

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.room.Room
import com.bogatti.ir.data.bogattiDatabase
import com.bogatti.ir.data.CreditManager
import com.bogatti.ir.service.AIService
import com.bogatti.ir.service.ModularConfigManager
import com.bogatti.ir.ui.screens.bogattiChatScreen
import com.bogatti.ir.ui.screens.bogattiAdminScreen
import com.bogatti.ir.ui.theme.bogattiTheme
import com.bogatti.ir.ui.viewmodel.bogattiViewModel

class MainActivity : ComponentActivity() {

    private lateinit var db: bogattiDatabase
    private lateinit var configManager: ModularConfigManager
    private lateinit var creditManager: CreditManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        db = Room.databaseBuilder(
            applicationContext,
            bogattiDatabase::class.java, "bogatti-db"
        ).build()

        configManager = ModularConfigManager(applicationContext)
        creditManager = CreditManager(applicationContext, encryptionKey = configManager.getAdminSecret())

        setContent {
            var currentScreen by remember { mutableStateOf("chat") }

            val useSSH = configManager.getString("use_ssh") == "true"
            val aiService = remember(useSSH) { AIService(useSSHBridge = useSSH) }

            // Standard ViewModel instantiation using Factory
            val vm: bogattiViewModel = viewModel(
                factory = object : ViewModelProvider.Factory {
                    override fun <T : ViewModel> create(modelClass: Class<T>): T {
                        return bogattiViewModel(db.chatDao(), aiService, creditManager, configManager) as T
                    }
                }
            )

            bogattiTheme {
                if (currentScreen == "chat") {
                    bogattiChatScreen(
                        viewModel = vm,
                        onOpenAdmin = { currentScreen = "admin" }
                    )
                } else {
                    bogattiAdminScreen(
                        configManager = configManager,
                        onClose = { currentScreen = "chat" }
                    )
                }
            }
        }
    }
}
