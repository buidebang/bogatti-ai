import React from 'react';
import { Message } from '../types';
import Markdown from 'react-markdown';
import { Bot, User } from 'lucide-react';
import { motion } from 'motion/react';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex w-full mb-6 px-4`}
    >
      <div className={`flex w-full max-w-[85%] gap-3 items-end ${isUser ? 'ms-auto flex-row-reverse' : 'me-auto flex-row'}`}>
        
        {/* Avatar */}
        <div className="flex-shrink-0 mb-1">
          {isUser ? (
             <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center border border-gray-600 shadow-sm">
                <User className="w-5 h-5 text-gray-300" />
             </div>
          ) : (
             <div className="w-8 h-8 rounded-full bg-bugatti flex items-center justify-center shadow-md shadow-bugatti/20">
                <Bot className="w-5 h-5 text-white" />
             </div>
          )}
        </div>

        {/* Bubble */}
        <div 
          className={`
            px-4 py-3 min-w-[60px] text-[15px] leading-relaxed
            ${isUser 
                ? 'bg-gray-700 text-gray-100 rounded-3xl rounded-br-sm' 
                : 'bg-transparent text-gray-100'
            }
          `}
        >
          {isUser ? (
            <div className="whitespace-pre-wrap">{message.content}</div>
          ) : (
            <div className="markdown-body prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-gray-800 prose-pre:border prose-pre:border-gray-700 prose-code:text-bugatti">
               <Markdown>{message.content || '...'}</Markdown>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

