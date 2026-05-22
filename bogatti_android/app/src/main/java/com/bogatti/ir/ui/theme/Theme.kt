package com.bogatti.ir.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val bogattiColorScheme = darkColorScheme(
    primary = SpotifyGreen,
    secondary = bogattiBlue,
    tertiary = SpotifyLightGray,
    background = SpotifyBlack,
    surface = SpotifyDarkGray,
    onPrimary = SpotifyBlack,
    onSecondary = SpotifyWhite,
    onTertiary = SpotifyWhite,
    onBackground = SpotifyWhite,
    onSurface = SpotifyWhite
)

@Composable
fun bogattiTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = bogattiColorScheme,
        typography = Typography,
        content = content
    )
}
