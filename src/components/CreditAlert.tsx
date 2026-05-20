import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Zap } from 'lucide-react';

interface CreditAlertProps {
  isVisible: boolean;
  credits: number;
}

export function CreditAlert({ isVisible, credits }: CreditAlertProps) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
           initial={{ opacity: 0, scale: 0.9, y: -10 }}
           animate={{ opacity: 1, scale: 1, y: 0 }}
           exit={{ opacity: 0, scale: 0.9, y: -10 }}
           className="absolute top-16 left-4 z-40" // Since it's RTL, top-left is visually top-right or just left
        >
            <div className="bg-gray-800 border border-gray-700 shadow-xl rounded-2xl p-3 flex flex-col gap-2 min-w-[160px]">
                <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-300 font-medium">موجودی شما</span>
                    <span className="text-xl font-bold font-mono text-white tracking-widest">{credits}</span>
                </div>
                
                {credits < 10 ? (
                    <motion.div 
                        animate={{ opacity: [1, 0.6, 1] }}
                        transition={{ repeat: Infinity, duration: 1.5 }}
                        className="text-xs text-red-400 font-medium text-center bg-red-950/40 rounded-lg py-1.5"
                    >
                        اعتبار رو به اتمام
                    </motion.div>
                ) : (
                    <div className="text-xs text-bugatti font-medium text-center bg-bugatti/10 rounded-lg py-1.5">
                        اشتراک فعال
                    </div>
                )}
                
                <button className="mt-1 w-full flex items-center justify-center gap-1 bg-gradient-to-r from-bugatti-dark to-bugatti hover:from-bugatti hover:to-bugatti-dark text-white text-sm font-medium py-2 rounded-xl transition-all shadow-md shadow-bugatti/20">
                    <Zap className="w-4 h-4" />
                    <span>شارژ آنی</span>
                </button>
            </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
