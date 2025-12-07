import { User, Bot } from "lucide-react";
import TypingIndicator from "./TypingIndicator";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  isTyping?: boolean;
  isError?: boolean;
}

interface ChatMessageProps {
  message: Message;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === "user";

  return (
    <div
      className={`message-enter flex gap-3 px-4 py-4 md:px-8 ${
        isUser ? "bg-transparent" : "bg-chat-area/50"
      }`}
    >
      <div
        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
          isUser
            ? "bg-chat-user text-chat-user-foreground"
            : "bg-chat-assistant text-chat-assistant-foreground"
        }`}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>

      <div className="flex-1 min-w-0">
        <p className="mb-1 text-xs font-medium text-muted-foreground">
          {isUser ? "You" : "Assistant"}
        </p>
        
        {message.isTyping ? (
          <TypingIndicator />
        ) : (
          <div
            className={`text-sm leading-relaxed ${
              message.isError
                ? "text-destructive"
                : isUser
                ? "text-foreground"
                : "text-chat-assistant-foreground"
            }`}
          >
            {message.content.split("\n").map((line, i) => (
              <p key={i} className={i > 0 ? "mt-2" : ""}>
                {line}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
