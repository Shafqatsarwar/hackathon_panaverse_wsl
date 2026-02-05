"use client";

import { useState, useEffect, useRef } from "react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function Home() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<any>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [isTyping, setIsTyping] = useState(false);
  const [activeTab, setActiveTab] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch System Status
  useEffect(() => {
    const fetchStatus = async () => {
      // Ensure client-side only
      if (typeof window === 'undefined') return;
      
      try {
        const res = await fetch("http://localhost:8000/api/status");
        if (res.ok) {
           const data = await res.json();
           setStatus(data);
        }
      } catch (e) {
        console.error("Failed to fetch status", e);
      }
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Poll every 30s
    return () => clearInterval(interval);
  }, []);

  // Initialize WebSocket
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/chat");

    socket.onopen = () => console.log("Connected to Chat Server");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "typing") {
        setIsTyping(true);
      } else if (data.type === "chunk") {
        setIsTyping(false);
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            return [...prev.slice(0, -1), { ...lastMsg, content: lastMsg.content + data.content }];
          } else {
            return [...prev, { role: "assistant", content: data.content }];
          }
        });
      } else if (data.type === "complete") {
        setIsTyping(false);
      } else if (data.type === "error") {
        setMessages((prev) => [...prev, { role: "system", content: `Error: ${data.message}` }]);
      }
    };

    socket.onclose = () => console.log("Disconnected");
    setWs(socket);

    return () => socket.close();
  }, []);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const sendMessage = async () => {
    if (!input.trim() || !ws) return;

    const userMsg = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);

    // Optimistic UI for User
    ws.send(JSON.stringify({ message: userMsg, user_id: "web-client" }));
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* Glass Header */}
      <header className="absolute top-0 w-full z-10 px-8 py-5 flex items-center justify-between backdrop-blur-md bg-black/10 border-b border-white/5">
        <div className="flex items-center gap-4">
          <div className="relative w-14 h-14 overflow-hidden rounded-2xl border border-white/20 shadow-lg shadow-purple-500/20 group">
            <img
              src="/Logo_Exellence.jpg"
              alt="Excellence Logo"
              className="object-cover w-full h-full transform group-hover:scale-110 transition-transform duration-500"
            />
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
              Panaversity Assistant
            </h1>
            <p className="text-sm text-gray-400 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              Powered by Gemini 2.5 & Odoo
            </p>
          </div>
        </div>

        <div className="flex gap-3">
          <StatusButton
            label="Odoo"
            active={status?.main_agent?.odoo_agent?.enabled}
            icon="📊"
            onClick={() => setActiveTab(activeTab === 'odoo' ? null : 'odoo')}
          />
          <StatusButton
            label="Email"
            active={status?.main_agent?.email_agent?.authenticated}
            icon="📧"
            onClick={() => setActiveTab(activeTab === 'email' ? null : 'email')}
          />
          <StatusButton
            label="WhatsApp"
            active={status?.main_agent?.whatsapp_agent?.enabled}
            icon="💬"
            onClick={() => setActiveTab(activeTab === 'whatsapp' ? null : 'whatsapp')}
          />
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-y-auto px-4 pt-32 pb-32 space-y-8 scroll-smooth">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-8 animate-[fadeInUp_0.8s_ease-out]">
            <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-blue-500/20 to-purple-600/20 border border-white/10 flex items-center justify-center backdrop-blur-xl shadow-2xl shadow-blue-500/20">
              <span className="text-5xl">🤖</span>
            </div>
            <div>
              <h2 className="text-4xl font-bold text-white mb-4">How can I help you?</h2>
              <p className="text-xl text-gray-400 max-w-lg mx-auto leading-relaxed">
                I can check your emails, update Odoo leads, or answer course questions.
              </p>
            </div>
            <div className="flex gap-4 flex-wrap justify-center">
              {['Check my unread emails', 'Update Odoo tasks', 'check my whatapp about any panaverse update'].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInput(suggestion)}
                  className="glass-button px-6 py-3 rounded-xl text-sm font-medium hover:text-blue-400 hover:border-blue-400/50 transition-all"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} px-4 md:px-20 animate-[fadeInUp_0.3s_ease-out]`}
          >
            <div
              className={`max-w-[70%] rounded-3xl px-8 py-6 text-lg shadow-xl backdrop-blur-md ${msg.role === "user"
                ? "bg-gradient-to-br from-blue-600 to-purple-700 text-white rounded-br-none border border-white/10"
                : "bg-zinc-800/80 text-gray-100 rounded-bl-none border border-white/10"
                }`}
            >

              <div className="whitespace-pre-wrap leading-relaxed message-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start px-4 md:px-20 animate-pulse">
            <div className="glass-panel rounded-3xl rounded-bl-none px-8 py-5 flex items-center gap-3">
              <div className="w-2.5 h-2.5 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-2.5 h-2.5 bg-purple-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-2.5 h-2.5 bg-pink-400 rounded-full animate-bounce"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Floating Input Area */}
      <footer className="absolute bottom-6 w-full px-4 flex justify-center z-20">
        <div className="w-full max-w-4xl glass-panel rounded-full p-2 pl-6 pr-2 flex items-center gap-4 input-glow transition-all duration-300">
          <input
            type="text"
            className="flex-1 bg-transparent text-xl text-white placeholder-gray-400 focus:outline-none py-4"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            autoFocus
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim()}
            className="h-14 w-14 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center hover:scale-105 active:scale-95 transition-transform disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/30"
          >
            <span className="text-2xl ml-1">➤</span>
          </button>
        </div>
      </footer>
    </div>
  );
}

function StatusButton({ label, active, icon, onClick }: { label: string; active: boolean; icon: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`
        glass-button flex items-center gap-2 px-4 py-2.5 rounded-xl border transition-all duration-300
        ${active ? "border-green-500/30 hover:border-green-500/50" : "border-red-500/30 hover:border-red-500/50"}
      `}
    >
      <span className="text-lg">{icon}</span>
      <span className="font-medium hidden md:inline">{label}</span>
      <span className={`w-2 h-2 rounded-full shadow-[0_0_8px_currentColor] ${active ? "bg-green-500 text-green-500" : "bg-red-500 text-red-500"}`} />
    </button>
  );
}
