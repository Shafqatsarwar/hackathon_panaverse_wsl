
import { useState, useEffect, useRef, useCallback } from 'react';

// Define Message Types
export interface Message {
    id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: number;
    status?: 'sending' | 'sent' | 'error';
}

interface UseChatOptions {
    apiEndpoint?: string;
    initialMessages?: Message[];
}

export const useChat = ({ apiEndpoint = '/api/chat', initialMessages = [] }: UseChatOptions = {}) => {
    const [messages, setMessages] = useState<Message[]>(initialMessages);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const socketRef = useRef<WebSocket | null>(null);

    // Initialize WebSocket (Optional: if we move to real-time)
    // For now, we will use standard fetch for stability as requested, 
    // but keeping structure ready for WS.

    const sendMessage = useCallback(async (content: string) => {
        if (!content.trim()) return;

        const newMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content,
            timestamp: Date.now(),
            status: 'sending'
        };

        setMessages(prev => [...prev, newMessage]);
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: content, history: messages })
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();

            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.response || "No response received.",
                timestamp: Date.now(),
                status: 'sent'
            };

            setMessages(prev => prev.map(m => m.id === newMessage.id ? { ...m, status: 'sent' as const } : m).concat(botMessage));

        } catch (err: any) {
            console.error("Chat Error:", err);
            setError(err.message || "Failed to send message");
            setMessages(prev => prev.map(m => m.id === newMessage.id ? { ...m, status: 'error' } : m));
        } finally {
            setIsLoading(false);
        }
    }, [apiEndpoint, messages]);

    const clearChat = useCallback(() => {
        setMessages([]);
    }, []);

    return {
        messages,
        isLoading,
        error,
        sendMessage,
        clearChat
    };
};
