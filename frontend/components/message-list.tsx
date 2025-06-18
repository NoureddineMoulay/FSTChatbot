"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import TypingIndicator from "./typing-indicator";

interface Message {
  id: string;
  content: string;
  sender: "user" | "bot";
  timestamp: Date;
}

interface MessageListProps {
  messages: Message[];
  isTyping: boolean;
}

function formatMessage(content: string) {
  // Split content into lines
  const lines = content.split("\n");

  // Process each line
  return lines.map((line, index) => {
    // Check if line is a list item (starts with number or bullet)
    if (/^\d+\./.test(line) || line.trim().startsWith("-")) {
      const listContent = line.replace(/^\d+\.\s*/, "");
      // Process names within list items
      const parts = listContent.split(/(Pr\.\s+[A-Za-z\s]+)/);
      return (
        <div key={index} className="flex items-start gap-2">
          <span className="text-gray-500 mt-1">
            {line.match(/^\d+\./)?.[0] || "•"}
          </span>
          <div>
            {parts.map((part, i) => {
              // Process bold text within list items
              const boldParts = part.split(/(\*\*.*?\*\*)/);
              return (
                <span key={i}>
                  {boldParts.map((boldPart, j) =>
                    boldPart.match(/\*\*.*?\*\*/) ? (
                      <span key={j} className="font-bold text-[#8A85FF]">
                        {boldPart.replace(/\*\*/g, "")}
                      </span>
                    ) : part.match(/Pr\.\s+[A-Za-z\s]+/) ? (
                      <span key={j} className="font-bold">
                        {part}
                      </span>
                    ) : (
                      <span key={j}>{boldPart}</span>
                    )
                  )}
                </span>
              );
            })}
          </div>
        </div>
      );
    }

    // Check if line contains an email
    if (line.includes("@")) {
      const parts = line.split(/(\S+@\S+\.\S+)/);
      return (
        <div key={index}>
          {parts.map((part, i) =>
            part.match(/\S+@\S+\.\S+/) ? (
              <a
                key={i}
                href={`mailto:${part}`}
                className="text-blue-600 hover:underline"
              >
                {part}
              </a>
            ) : (
              <span key={i}>{part}</span>
            )
          )}
        </div>
      );
    }

    // Process names and bold text in regular text
    const parts = line.split(/(Pr\.\s+[A-Za-z\s]+|\*\*.*?\*\*)/);
    return (
      <div key={index}>
        {parts.map((part, i) => {
          if (part.match(/\*\*.*?\*\*/)) {
            return (
              <span key={i} className="font-bold text-[#8A85FF]">
                {part.replace(/\*\*/g, "")}
              </span>
            );
          } else if (part.match(/Pr\.\s+[A-Za-z\s]+/)) {
            return (
              <span key={i} className="font-bold">
                {part}
              </span>
            );
          } else {
            return <span key={i}>{part}</span>;
          }
        })}
      </div>
    );
  });
}

export default function MessageList({ messages, isTyping }: MessageListProps) {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <motion.div
          key={message.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className={cn(
            "flex",
            message.sender === "user" ? "justify-end" : "justify-start"
          )}
        >
          <div
            className={cn(
              "max-w-[80%] rounded-2xl px-4 py-2 shadow-sm",
              message.sender === "user"
                ? "bg-[#8A85FF] text-white rounded-tr-none"
                : "bg-white border border-gray-100 rounded-tl-none"
            )}
          >
            <div
              className={cn(
                "text-sm space-y-1",
                message.sender === "user" ? "text-white" : "text-gray-800"
              )}
            >
              {formatMessage(message.content)}
            </div>
            <div
              className={cn(
                "text-[10px] mt-1",
                message.sender === "user" ? "text-purple-200" : "text-gray-400"
              )}
            >
              {message.timestamp.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </div>
          </div>
        </motion.div>
      ))}

      {isTyping && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-start"
        >
          <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-none px-4 py-2 shadow-sm">
            <TypingIndicator />
          </div>
        </motion.div>
      )}
    </div>
  );
}
