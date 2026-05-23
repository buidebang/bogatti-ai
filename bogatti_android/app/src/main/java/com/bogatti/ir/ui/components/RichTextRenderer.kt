package com.bogatti.ir.ui.components

import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.bogatti.ir.ui.theme.*

@Composable
fun RichTextRenderer(text: String, isUser: Boolean) {
    // A simplified composite renderer that breaks down the message into segments
    // In a production app, this would be a full Markdown parser visitor.

    val segments = text.split(Regex("(?=```)|(?<=```)|(?=\\$\\$)|(?<=\\$\\$)"))

    Column {
        var inCodeBlock = false
        var inLaTeXBlock = false

        segments.forEach { segment ->
            when {
                segment == "```" -> {
                    inCodeBlock = !inCodeBlock
                }
                segment == "$$" -> {
                    inLaTeXBlock = !inLaTeXBlock
                }
                inCodeBlock -> {
                    CodeBlock(segment.trim())
                }
                inLaTeXBlock -> {
                    LaTeXRenderer("$$" + segment + "$$")
                }
                segment.isNotBlank() -> {
                    Text(
                        text = TypographyEngine.formatMixedText(segment),
                        color = SpotifyWhite,
                        style = Typography.bodyLarge
                    )
                }
            }
        }
    }
}

@Composable
fun CodeBlock(code: String) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
            .clip(RoundedCornerShape(8.dp))
            .background(SpotifyBlack)
            .padding(12.dp)
    ) {
        // Simulating syntax highlighting with colors for keywords
        val highlighted = buildCodeAnnotatedString(code)
        Text(
            text = highlighted,
            fontFamily = JetBrainsMono
        )
    }
}

fun buildCodeAnnotatedString(code: String) = androidx.compose.ui.text.buildAnnotatedString {
    val keywords = listOf("val", "var", "fun", "class", "import", "package", "return", "if", "else", "when")
    val parts = code.split(Regex("(?<=\\W)|(?=\\W)"))
    parts.forEach { part ->
        when {
            part in keywords -> {
                pushStyle(androidx.compose.ui.text.SpanStyle(color = Color(0xFFC792EA))) // Purple
                append(part)
                pop()
            }
            part.toIntOrNull() != null -> {
                pushStyle(androidx.compose.ui.text.SpanStyle(color = Color(0xFFF78C6C))) // Orange
                append(part)
                pop()
            }
            part.startsWith("\"") && part.endsWith("\"") -> {
                pushStyle(androidx.compose.ui.text.SpanStyle(color = Color(0xFFC3E88D))) // Green
                append(part)
                pop()
            }
            else -> {
                append(part)
            }
        }
    }
}

@Composable
fun LaTeXRenderer(latex: String) {
    AndroidView(
        factory = { context ->
            WebView(context).apply {
                webViewClient = WebViewClient()
                settings.javaScriptEnabled = true
                backgroundColor = 0x00000000 // Transparent
                loadDataWithBaseURL(
                    null,
                    """
                    <html>
                    <head>
                        <script type="text/javascript" async
                          src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-MML-AM_CHTML">
                        </script>
                        <style>
                            body { color: white; background-color: transparent; font-size: 16px; margin: 0; padding: 0; }
                        </style>
                    </head>
                    <body>
                        $latex
                    </body>
                    </html>
                    """.trimIndent(),
                    "text/html",
                    "UTF-8",
                    null
                )
            }
        },
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 40.dp, max = 400.dp)
    )
}
