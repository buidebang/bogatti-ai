package com.bogatti.ir.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.bogatti.ir.ui.theme.*
import com.bogatti.ir.service.ModularConfigManager

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun bogattiAdminScreen(configManager: ModularConfigManager, onClose: () -> Unit) {
    var appTitle by remember { mutableStateOf(configManager.getString("app_title", "bogatti")) }
    var tomanRate by remember { mutableStateOf(configManager.getTomanRate().toString()) }
    var apiKey by remember { mutableStateOf(configManager.getString("api_key")) }
    var modelSelection by remember { mutableStateOf(configManager.getString("current_model", "gemini-pro")) }
    var useSSH by remember { mutableStateOf(configManager.getString("use_ssh") == "true") }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("bogatti Admin Dashboard", color = SpotifyWhite) },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = SpotifyDarkGray
                )
            )
        },
        containerColor = SpotifyBlack
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
                .padding(16.dp)
        ) {
            item {
                AdminInputSection("App Title", appTitle) { appTitle = it }
                AdminInputSection("Toman per USD", tomanRate) { tomanRate = it }
                AdminInputSection("API Key", apiKey) { apiKey = it }
                AdminInputSection("Default Model", modelSelection) { modelSelection = it }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("SSH Bridge Mode", color = SpotifyWhite)
                    Switch(
                        checked = useSSH,
                        onCheckedChange = { useSSH = it },
                        colors = SwitchDefaults.colors(checkedThumbColor = SpotifyGreen)
                    )
                }

                Spacer(modifier = Modifier.height(24.dp))

                Button(
                    onClick = {
                        configManager.setString("app_title", appTitle)
                        configManager.setTomanRate(tomanRate.toIntOrNull() ?: 100000)
                        configManager.setString("api_key", apiKey)
                        configManager.setString("current_model", modelSelection)
                        configManager.setString("use_ssh", useSSH.toString())
                    },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = SpotifyGreen)
                ) {
                    Text("Save Changes", color = SpotifyBlack)
                }

                TextButton(
                    onClick = onClose,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Close", color = SpotifyGrayText)
                }
            }
        }
    }
}

@Composable
fun AdminInputSection(label: String, value: String, onValueChange: (String) -> Unit) {
    Column(modifier = Modifier.padding(vertical = 8.dp)) {
        Text(text = label, color = SpotifyGrayText, style = MaterialTheme.typography.labelMedium)
        TextField(
            value = value,
            onValueChange = onValueChange,
            modifier = Modifier.fillMaxWidth(),
            colors = TextFieldDefaults.colors(
                focusedContainerColor = SpotifyDarkGray,
                unfocusedContainerColor = SpotifyDarkGray,
                focusedTextColor = SpotifyWhite,
                unfocusedTextColor = SpotifyWhite
            )
        )
    }
}
