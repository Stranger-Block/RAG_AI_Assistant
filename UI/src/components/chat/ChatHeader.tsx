import { Bot, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import SettingsPanel from "./SettingsPanel";
import { ChatSettings } from "@/lib/chatApi";

interface ChatHeaderProps {
  onSettingsChange: (settings: ChatSettings) => void;
  onClearChat: () => void;
  messageCount: number;
}

const ChatHeader = ({ onSettingsChange, onClearChat, messageCount }: ChatHeaderProps) => {
  return (
    <header className="flex items-center justify-between border-b border-border bg-card/50 px-4 py-3 backdrop-blur-sm">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10">
          <Bot className="h-5 w-5 text-primary" />
        </div>
        <div>
          <h1 className="text-sm font-semibold text-foreground">RAG Assistant</h1>
          <p className="text-xs text-muted-foreground">Powered by your knowledge base</p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {messageCount > 0 && (
          <Button
            variant="ghost"
            size="icon"
            onClick={onClearChat}
            className="h-9 w-9 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
          >
            <Trash2 className="h-5 w-5" />
          </Button>
        )}
        <SettingsPanel onSettingsChange={onSettingsChange} />
      </div>
    </header>
  );
};

export default ChatHeader;
