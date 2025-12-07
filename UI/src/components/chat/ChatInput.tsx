import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

const ChatInput = ({ onSend, disabled }: ChatInputProps) => {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  }, [input]);

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-border bg-chat-input p-4">
      <div className="mx-auto max-w-3xl">
        <div className="flex items-end gap-3 rounded-xl border border-border bg-input p-3 focus-within:border-primary/50 focus-within:ring-1 focus-within:ring-primary/30 transition-all">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Send a message..."
            disabled={disabled}
            rows={1}
            className="flex-1 resize-none bg-transparent text-sm text-foreground placeholder:text-muted-foreground focus:outline-none disabled:opacity-50 scrollbar-thin"
          />
          <Button
            onClick={handleSubmit}
            disabled={!input.trim() || disabled}
            size="icon"
            className="h-8 w-8 shrink-0 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-40 glow-primary transition-all"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
        <p className="mt-2 text-center text-xs text-muted-foreground">
          AI can make mistakes. Consider verifying important information.
        </p>
      </div>
    </div>
  );
};

export default ChatInput;
