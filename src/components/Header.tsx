import React from 'react';
import { Menu, Edit } from 'lucide-react';
import { MODELS } from '../types';

interface HeaderProps {
  onMenuClick: () => void;
  onNewChat: () => void;
  activeModelId: string;
  onModelChange: (id: string) => void;
}

export function Header({ onMenuClick, onNewChat, activeModelId, onModelChange }: HeaderProps) {
  const activeModel = MODELS.find(m => m.id === activeModelId) || MODELS[0];

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between px-4 h-14 bg-gray-900 border-b border-gray-800">
      
      <button 
        onClick={onMenuClick}
        className="p-2 -mr-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-full transition-colors flex-shrink-0"
      >
        <Menu className="w-6 h-6" />
      </button>

      {/* Model Selector Array Pattern */}
      <div className="flex-1 flex justify-center">
         <div className="relative group cursor-pointer">
             <div className="flex items-center gap-2 bg-gray-800/50 hover:bg-gray-800 px-4 py-1.5 rounded-xl transition-colors">
                <span className="font-semibold text-gray-200 text-[15px]">{activeModel.name}</span>
                <svg className="w-4 h-4 text-gray-400 group-hover:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
             </div>
             
             {/* Dropdown via hover for simplicity (or state, but simple for now) */}
             <div className="absolute top-full mt-2 left-1/2 -translate-x-1/2 w-48 bg-gray-800 border border-gray-700 rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 overflow-hidden">
                {MODELS.map(model => (
                    <button
                        key={model.id}
                        className={`w-full text-right px-4 py-3 text-sm hover:bg-gray-700 transition-colors flex items-center justify-between ${model.id === activeModelId ? 'text-bugatti' : 'text-gray-200'}`}
                        onClick={(e) => {
                             e.stopPropagation();
                             onModelChange(model.id);
                        }}
                    >
                        <span>{model.name}</span>
                        {model.id === activeModelId && <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>}
                    </button>
                ))}
             </div>
         </div>
      </div>

      <button 
        onClick={onNewChat}
        className="p-2 -ml-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-full transition-colors flex-shrink-0"
      >
        <Edit className="w-5 h-5" />
      </button>

    </header>
  );
}
