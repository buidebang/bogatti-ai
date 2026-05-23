package com.bogatti.ir.ui.screens

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.bogatti.ir.ui.components.RichTextRenderer
import com.bogatti.ir.ui.theme.*
import com.bogatti.ir.ui.viewmodel.bogattiViewModel

@Composable
fun bogattiChatScreen(viewModel: bogattiViewModel, onOpenAdmin: () -> Unit) {
    val messages by viewModel.chatHistory.collectAsState(initial = emptyList())
    val isLoading by viewModel.isLoading.collectAsState()
    val balance by viewModel.balance.collectAsState()
    val appTitle = viewModel.getAppTitle()
    var inputText by remember { mutableStateOf("") }
    val listState = rememberLazyListState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(SpotifyBlack)
    ) {
        // Spotify-style Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = appTitle,
                color = SpotifyWhite,
                fontSize = 24.sp,
                fontFamily = FontFamily.SansSerif,
                modifier = Modifier.clickable { onOpenAdmin() }
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "$$balance",
                    color = SpotifyGreen,
                    fontSize = 14.sp
                )
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(onClick = onOpenAdmin) {
                    Icon(
                        imageVector = Icons.Default.Settings,
                        contentDescription = "Settings",
                        tint = SpotifyGrayText
                    )
                }
            }
        }

        // Chat Log
        LazyColumn(
            state = listState,
            modifier = Modifier
                .weight(1fr)
                .fillMaxWidth()
                .padding(horizontal = 8.dp)
        ) {
            items(messages) { msg ->
                ChatBubble(msg.text, msg.sender == "user")
            }
            if (isLoading) {
                item { SpotifyWaveformLoading() }
            }
        }

        // Auto-scroll to bottom
        LaunchedEffect(messages.size, isLoading) {
            if (messages.isNotEmpty()) {
                listState.animateScrollToItem(messages.size)
            }
        }

        // Input Area
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextField(
                value = inputText,
                onValueChange = { inputText = it },
                placeholder = { Text("Ask bogatti...", color = SpotifyGrayText) },
                modifier = Modifier
                    .weight(1fr)
                    .clip(RoundedCornerShape(24.dp)),
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = SpotifyLightGray,
                    unfocusedContainerColor = SpotifyLightGray,
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent,
                    focusedTextColor = SpotifyWhite,
                    unfocusedTextColor = SpotifyWhite
                )
            )
            Spacer(modifier = Modifier.width(8.dp))
            Button(
                onClick = {
                    if (inputText.isNotBlank()) {
                        viewModel.sendMessage(inputText)
                        inputText = ""
                    }
                },
                colors = ButtonDefaults.buttonColors(containerColor = SpotifyGreen),
                shape = RoundedCornerShape(24.dp)
            ) {
                Text("Send", color = SpotifyBlack)
            }
        }
    }
}

@Composable
fun SpotifyWaveformLoading() {
    val infiniteTransition = rememberInfiniteTransition(label = "waveform")
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically
    ) {
        repeat(5) { i ->
            val height by infiniteTransition.animateFloat(
                initialValue = 10f,
                targetValue = 40f,
                animationSpec = infiniteRepeatable(
                    animation = tween(500, delayMillis = i * 100, easing = LinearEasing),
                    repeatMode = RepeatMode.Reverse
                ),
                label = "bar_$i"
            )
            Box(
                modifier = Modifier
                    .width(4.dp)
                    .height(height.dp)
                    .padding(horizontal = 1.dp)
                    .background(SpotifyGreen, RoundedCornerShape(2.dp))
            )
        }
    }
}

@Composable
fun ChatBubble(text: String, isUser: Boolean) {
    val alignment = if (isUser) Alignment.End else Alignment.Start
    val bgColor = if (isUser) SpotifyLightGray else SpotifyDarkGray
    val textColor = SpotifyWhite

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        horizontalAlignment = alignment
    ) {
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(12.dp))
                .background(bgColor)
                .padding(12.dp)
        ) {
            RichTextRenderer(text = text, isUser = isUser)
        }
    }
}
