"use client";

import type React from "react";

import { useState } from "react";
import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
}

export default function ChatInput({ onSendMessage }: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-4 border-t border-gray-200 bg-white"
    >
      <div className="flex items-end gap-2">
        <div className="relative flex-1">
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Tapez votre message..."
            className="min-h-[50px] max-h-[150px] pr-10 resize-none rounded-xl border-gray-200 focus-visible:ring-[#8A85FF]"
          />
        </div>
        <Button
          type="submit"
          className="bg-[#8A85FF] hover:bg-[#7A75EF] rounded-xl h-10 w-10 p-0 flex items-center justify-center"
          disabled={!message.trim()}
        >
          <Send className="h-5 w-5" />
        </Button>
      </div>
      <div className="text-xs text-gray-400 mt-2 text-center">
        Posez des questions sur les heures de bureau, les ressources du
        département ou les politiques académiques
      </div>
    </form>
  );
}
