"use client";

import React, { useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function page() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Send user message to backend LLM API
    const response = await fetch(
      "https://5dd0-35-196-68-55.ngrok-free.app/query",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage.content }),
      }
    );

    const data = await response.json();

    const assistantMessage: Message = {
      role: "assistant",
      content: data.answer,
    };
    setMessages((prev) => [...prev, assistantMessage]);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4 ">
      <div className="mt-[50px] text-center text-[50px] text-transparent bg-clip-text bg-gradient-to-r from-orange-100 to-orange-300 font-bold  leading-[1.2] max-w-[850px] mx-auto">
        Welcome To Your Personal AI Email Assistant
      </div>
      {messages.length > 0 ? (
        <div
          className={`overflow-y-auto  mb-4 space-y-4 bg-black mt-[100px] transition-all duration-500`}
          style={{
            height: `${Math.min(
              100 + messages.length * 60,
              window.innerHeight * 0.7
            )}px`, // grows 60px per msg, capped at 70vh
          }}
        >
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-xs px-4 py-2 rounded-2xl ${
                  msg.role === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-white border text-gray-800"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="mt-[100px] mb-[100px] text-center text-[30px] text-transparent bg-clip-text bg-gradient-to-r from-yellow-100 to-yellow-300 font-bold leading-[1.2] max-w-[850px] mx-auto">
          How can I help you today?
        </div>
      )}

      <div className="flex flex-col">
        <textarea
          className="border rounded-lg p-2 resize-none h-24"
          placeholder="Type your message here..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          onClick={sendMessage}
          className="mt-2 bg-black text-white px-4 py-2 rounded-lg self-end"
        >
          Send
        </button>
      </div>
    </div>
  );
}
