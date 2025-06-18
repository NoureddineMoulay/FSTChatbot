"use client"

import { motion } from "framer-motion"

export default function TypingIndicator() {
  return (
    <div className="flex items-center space-x-1.5 px-1 py-1">
      {[0, 1, 2].map((dot) => (
        <motion.div
          key={dot}
          className="w-2 h-2 rounded-full bg-[#2DD4BF]"
          initial={{ opacity: 0.4 }}
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{
            duration: 1.2,
            repeat: Number.POSITIVE_INFINITY,
            delay: dot * 0.2,
          }}
        />
      ))}
    </div>
  )
}
