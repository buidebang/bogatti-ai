import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Helper to initialize Gemini API on demand
  let _ai: GoogleGenAI | null = null;
  function getAI(): GoogleGenAI {
    if (!_ai) {
      const apiKey = process.env.GEMINI_API_KEY;
      if (!apiKey) {
        throw new Error("GEMINI_API_KEY is missing");
      }
      _ai = new GoogleGenAI({ apiKey });
    }
    return _ai;
  }

  // Handle Chat API requests
  app.post("/api/chat", async (req, res) => {
    try {
      const { messages, modelId = "gemini-3.1-pro-preview" } = req.body;
      if (!messages || !Array.isArray(messages)) {
        res.status(400).json({ error: "Invalid messages array." });
        return;
      }
      
      const ai = getAI();
      
      // Formatting messages for Gemini SDK: array of { role: 'user' | 'model', parts: [{ text: string }] }
      const formattedMessages = messages.map(msg => ({
        role: msg.role === "assistant" ? "model" : "user",
        parts: [{ text: msg.content }]
      }));

      // Find the last user message and the history
      const lastMessage = formattedMessages.pop();
      if (!lastMessage || lastMessage.role !== "user") {
        throw new Error("Last message must be from user.");
      }

      const responseStream = await ai.models.generateContentStream({
        model: modelId,
        contents: [
            ...formattedMessages,
            lastMessage
        ],
        config: {
            systemInstruction: "شما یک دستیار هوش مصنوعی هوشمند، مودب و دقیق هستید. لطفا به زبان فارسی و با ادبیات مناسب پاسخ دهید.",
            temperature: 0.7,
        }
      });

      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');

      for await (const chunk of responseStream) {
        if (chunk.text) {
           const data = JSON.stringify({ text: chunk.text });
           res.write(`data: ${data}\n\n`);
        }
      }
      
      res.write('data: [DONE]\n\n');
      res.end();

    } catch (error: any) {
      console.error("Chat API Error:", error);
      if (!res.headersSent) {
          res.status(500).json({ error: error.message || "Internal server error" });
      } else {
          res.end();
      }
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();
