import { useState, useRef, useEffect, useCallback } from "react";
import ChatHeader from "@/components/chat/ChatHeader";
import ChatMessage, { Message } from "@/components/chat/ChatMessage";
import ChatInput from "@/components/chat/ChatInput";
import EmptyState from "@/components/chat/EmptyState";
import { ChatSettings, getSettings, sendMessage } from "@/lib/chatApi";

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [settings, setSettings] = useState<ChatSettings>(getSettings);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSend = async (content: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content,
    };

    const typingMessage: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "",
      isTyping: true,
    };

    setMessages((prev) => [...prev, userMessage, typingMessage]);
    setIsLoading(true);

    try {
      const answer = await sendMessage(content, settings);

      setMessages((prev) => {
        const updated = [...prev];
        const typingIndex = updated.findIndex((m) => m.isTyping);
        if (typingIndex !== -1) {
          updated[typingIndex] = {
            ...updated[typingIndex],
            content: answer,
            isTyping: false,
          };
        }
        return updated;
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "An unexpected error occurred";

      setMessages((prev) => {
        const updated = [...prev];
        const typingIndex = updated.findIndex((m) => m.isTyping);
        if (typingIndex !== -1) {
          updated[typingIndex] = {
            ...updated[typingIndex],
            content: `Error: ${errorMessage}. Please check your API settings and try again.`,
            isTyping: false,
            isError: true,
          };
        }
        return updated;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="flex h-screen flex-col bg-background">
      <ChatHeader
        onSettingsChange={setSettings}
        onClearChat={handleClearChat}
        messageCount={messages.length}
      />

      <main className="flex-1 overflow-y-auto scrollbar-thin">
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="mx-auto max-w-3xl">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
};

export default Index;
