import React, { useState, useRef, useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { MessageInput } from './components/MessageInput';
import { ChatMessage } from './components/ChatMessage';
import { CreditAlert } from './components/CreditAlert';
import { Message, MODELS } from './types';
import { Bot } from 'lucide-react';
import { motion } from 'motion/react';

export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [activeModelId, setActiveModelId] = useState(MODELS[0].id);
  const [credits, setCredits] = useState(42);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = async (content: string) => {
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          modelId: activeModelId,
          messages: [...messages, userMsg].map(m => ({ role: m.role, content: m.content })),
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      setMessages(prev => [...prev, { id: 'loading', role: 'assistant', content: '' }]);

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantMsgContent = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ') && line !== 'data: [DONE]') {
              try {
                const data = JSON.parse(line.slice(6));
                assistantMsgContent += data.text;
                
                setMessages(prev => {
                  const updated = [...prev];
                  const last = updated[updated.length - 1];
                  if (last.id === 'loading') {
                    last.content = assistantMsgContent;
                  }
                  return updated;
                });
              } catch (e) {
                console.error("Parse error", e);
              }
            }
          }
        }
      }

      setMessages(prev => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last.id === 'loading') {
           last.id = Date.now().toString();
        }
        return updated;
      });

      // Deduct credits based on active model cost
      const activeModel = MODELS.find(m => m.id === activeModelId);
      if (activeModel) {
          setCredits(c => Math.max(0, c - activeModel.creditCost));
      }

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'assistant', content: 'خطا در ارتباط با سرور. لطفا مجددا تلاش کنید.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="h-screen w-full flex flex-col bg-gray-900 overflow-hidden relative">
      
      {/* Absolute Neon Popup */}
      <CreditAlert isVisible={true} credits={credits} />

      <Sidebar 
        isOpen={isSidebarOpen} 
        onClose={() => setIsSidebarOpen(false)} 
        credits={credits}
      />

      <Header 
        onMenuClick={() => setIsSidebarOpen(true)}
        onNewChat={handleNewChat}
        activeModelId={activeModelId}
        onModelChange={setActiveModelId}
      />

      {/* Main Chat Area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto scroll-smooth pb-4 pt-8"
      >
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center p-8">
            <motion.div 
               initial={{ scale: 0.5, opacity: 0 }}
               animate={{ scale: 1, opacity: 1 }}
               transition={{ type: 'spring', bounce: 0.5 }}
               className="w-20 h-20 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center shadow-2xl mb-6 relative"
            >
               <Bot className="w-10 h-10 text-bugatti" />
               <div className="absolute inset-0 rounded-full border-2 border-bugatti opacity-20 animate-ping" />
            </motion.div>
            <h1 className="text-2xl font-bold text-white mb-2">بوگاتی، دستیار هوشمند شما</h1>
            <p className="text-gray-400 text-center max-w-xs text-sm leading-relaxed">
              با استفاده از پیشرفته‌ترین مدل‌های زبانی جهان، پاسخ سوالات خود را پیدا کنید.
            </p>
          </div>
        ) : (
          messages.map(msg => (
            <ChatMessage key={msg.id} message={msg} />
          ))
        )}
      </div>

      {/* Fixed Bottom Input */}
      <MessageInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
}

