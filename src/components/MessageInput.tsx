import React, { useRef, useEffect } from 'react';
import { Send, Plus, Mic } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

interface MessageInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

export function MessageInput({ onSend, isLoading }: MessageInputProps) {
  const [text, setText] = React.useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      // Max height approx 5 lines
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [text]);

  const handleSend = () => {
    const trimmed = text.trim();
    if (trimmed && !isLoading) {
      onSend(trimmed);
      setText('');
      if (textareaRef.current) {
         textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full px-4 pb-4 pt-2">
      <div className="relative flex items-end bg-gray-800 rounded-3xl p-1 gap-2 mx-auto max-w-3xl border border-gray-700/50 shadow-lg">
        
        <button className="flex-shrink-0 p-3 bg-gray-700/50 rounded-full text-gray-300 hover:text-white hover:bg-gray-600 transition-colors">
            <Plus className="w-5 h-5" />
        </button>

        <textarea
          ref={textareaRef}
          dir="auto"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="پیام بدهید..."
          className="flex-1 max-h-32 min-h-[44px] py-3 bg-transparent text-gray-100 placeholder-gray-400 resize-none outline-none text-[15px] leading-relaxed"
          rows={1}
        />

        <div className="flex flex-shrink-0 mb-1 ml-1 items-center justify-center">
            {text.trim() ? (
                <button
                    onClick={handleSend}
                    disabled={isLoading}
                    className="p-2 bg-bugatti rounded-full text-white hover:bg-bugatti-dark transition-all disabled:opacity-50 flex items-center justify-center h-10 w-10 shadow-md"
                >
                    <Send className="w-5 h-5 ml-0.5" />
                </button>
            ) : (
                <button className="p-2 bg-transparent rounded-full text-gray-300 hover:text-white transition-all flex items-center justify-center h-10 w-10">
                    <Mic className="w-5 h-5" />
                </button>
            )}
        </div>
      </div>
      <div className="text-center mt-2">
         <span className="text-[10px] text-gray-500">بوگاتی می‌تواند اشتباه کند. اطلاعات مهم را بررسی کنید.</span>
      </div>
    </div>
  );
}
