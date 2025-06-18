"use client";

import { X, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ChatHeaderProps {
  onClose: () => void;
}

export default function ChatHeader({ onClose }: ChatHeaderProps) {
  return (
    <div className="bg-[#0E1117] text-white p-4 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="bg-[#8A85FF] p-1.5 rounded-md">
          <Bot className="h-5 w-5" />
        </div>
        <div>
          <h3 className="font-medium">Assistant de la Faculté</h3>
          <div className="text-xs text-gray-300 flex items-center gap-1">
            <span className="inline-block w-1.5 h-1.5 bg-green-400 rounded-full"></span>
            <span>Propulsé par l'IA</span>
          </div>
        </div>
      </div>
      <Button
        variant="ghost"
        size="icon"
        onClick={onClose}
        className="text-gray-300 hover:text-white hover:bg-[#1A1D25]"
      >
        <X className="h-5 w-5" />
      </Button>
    </div>
  );
}
