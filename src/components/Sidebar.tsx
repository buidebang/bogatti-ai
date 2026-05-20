import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, Settings, Zap, History, MessageSquare } from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  credits: number;
}

export function Sidebar({ isOpen, onClose, credits }: SidebarProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 z-40 backdrop-blur-sm"
          />

          {/* Drawer (RTL -> slides from right) */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: "spring", bounce: 0, duration: 0.3 }}
            className="fixed inset-y-0 right-0 w-[80%] max-w-sm bg-gray-900 border-l border-gray-800 z-50 flex flex-col shadow-2xl"
          >
            {/* User Profile / Logo */}
            <div className="p-4 border-b border-gray-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-bugatti flex items-center justify-center font-bold text-white shadow-md shadow-bugatti/20">
                        B
                    </div>
                    <div>
                        <h2 className="font-bold text-gray-100 uppercase tracking-wider text-sm">Bugatti Ai</h2>
                        <p className="text-xs text-gray-400">حساب ویژه</p>
                    </div>
                </div>
                <button onClick={onClose} className="p-2 text-gray-400 hover:text-white rounded-full">
                    <X className="w-5 h-5" />
                </button>
            </div>

            {/* History / Chat List */}
            <div className="flex-1 overflow-y-auto p-3">
                <div className="text-xs font-semibold text-gray-500 mb-2 px-1">امروز</div>
                <button className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 text-gray-300 transition-colors">
                    <MessageSquare className="w-4 h-4 text-gray-500" />
                    <span className="text-sm truncate">راهنمای برنامه نویسی پایتون</span>
                </button>
                <div className="text-xs font-semibold text-gray-500 mt-4 mb-2 px-1">دیروز</div>
                <button className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-800 text-gray-300 transition-colors">
                    <MessageSquare className="w-4 h-4 text-gray-500" />
                    <span className="text-sm truncate">طراحی رابط کاربری بوگاتی</span>
                </button>
            </div>

            {/* Footer Items */}
            <div className="p-3 border-t border-gray-800 space-y-1">
                <button className="w-full flex items-center gap-3 p-3 text-sm text-bugatti font-medium hover:bg-gray-800 rounded-xl transition-colors">
                    <Zap className="w-5 h-5" />
                    <span>خرید اعتبار / {credits} کلید</span>
                </button>
                <button className="w-full flex items-center gap-3 p-3 text-sm text-gray-300 hover:bg-gray-800 rounded-xl transition-colors">
                    <History className="w-5 h-5" />
                    <span>تاریخچه تراکنش‌ها</span>
                </button>
                <button className="w-full flex items-center gap-3 p-3 text-sm text-gray-300 hover:bg-gray-800 rounded-xl transition-colors">
                    <Settings className="w-5 h-5" />
                    <span>تنظیمات</span>
                </button>
            </div>

          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
