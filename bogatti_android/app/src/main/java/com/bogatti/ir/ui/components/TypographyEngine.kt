package com.bogatti.ir.ui.components

import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import com.bogatti.ir.ui.theme.JetBrainsMono
import com.bogatti.ir.ui.theme.SpotifyGreen
import java.util.regex.Pattern

object TypographyEngine {
    private val englishPattern = Pattern.compile("[\\x00-\\x7F]+")

    /**
     * Scans the input string and applies JetBrains Mono to English/LTR text
     * and Vazirmatn (default) to Persian/RTL text.
     */
    fun formatMixedText(text: String): AnnotatedString {
        return buildAnnotatedString {
            val matcher = englishPattern.matcher(text)
            var lastIndex = 0

            while (matcher.find()) {
                // Add the Persian text before the match
                if (matcher.start() > lastIndex) {
                    append(text.substring(lastIndex, matcher.start()))
                }

                // Add the English match with Mono font and subtle color
                val englishText = matcher.group()
                pushStyle(
                    SpanStyle(
                        fontFamily = JetBrainsMono,
                        color = SpotifyGreen.copy(alpha = 0.9f),
                        fontWeight = FontWeight.Medium
                    )
                )
                append(englishText)
                pop()

                lastIndex = matcher.end()
            }

            // Add remaining Persian text
            if (lastIndex < text.length) {
                append(text.substring(lastIndex))
            }
        }
    }
}
