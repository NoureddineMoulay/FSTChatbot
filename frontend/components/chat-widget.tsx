"use client";

import { useState, useRef, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { MessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import ChatHeader from "./chat-header";
import MessageList from "./message-list";
import ChatInput from "./chat-input";
import { cn } from "@/lib/utils";

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<
    Array<{
      id: string;
      content: string;
      sender: "user" | "bot";
      timestamp: Date;
    }>
  >([
    {
      id: "1",
      content:
        "Bonjour ! Je suis votre assistant de la faculté. Comment puis-je vous aider aujourd'hui ?",
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [sessionId] = useState(() => crypto.randomUUID());

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Add user message
    const newUserMessage = {
      id: Date.now().toString(),
      content: message,
      sender: "user" as const,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newUserMessage]);
    setIsTyping(true);

    try {
      const response = await fetch("http://localhost:8001/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: message,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error("Échec de la réponse du serveur");
      }

      const data = await response.json();

      const newBotMessage = {
        id: (Date.now() + 1).toString(),
        content: data.answer,
        sender: "bot" as const,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, newBotMessage]);
    } catch (error) {
      console.error("Erreur lors de l'envoi du message:", error);
      // Add error message
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        content:
          "Désolé, j'ai rencontré une erreur. Veuillez réessayer plus tard.",
        sender: "bot" as const,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <>
      {/* Chat Button */}
      <motion.div
        className={cn(
          "fixed bottom-6 right-6 z-50",
          isOpen ? "hidden" : "block"
        )}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Button
          onClick={toggleChat}
          className="w-16 h-16 rounded-full bg-[#0E1117] hover:bg-[#0E1117]/90 text-white shadow-lg flex items-center justify-center"
        >
          <MessageSquare className="h-7 w-7" />
        </Button>
      </motion.div>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-0 right-0 z-50 w-full sm:w-[400px] h-[600px] max-h-[calc(100vh-2rem)] sm:bottom-6 sm:right-6 rounded-t-lg sm:rounded-lg overflow-hidden shadow-2xl bg-white border border-gray-200"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 20, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="flex flex-col h-full">
              <ChatHeader onClose={toggleChat} />

              <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
                <MessageList messages={messages} isTyping={isTyping} />
                <div ref={messagesEndRef} />
              </div>

              <ChatInput onSendMessage={handleSendMessage} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
