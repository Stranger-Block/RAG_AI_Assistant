import { MessageSquare, Sparkles, BookOpen } from "lucide-react";

const EmptyState = () => {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-4 py-12">
      <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 glow-primary">
        <MessageSquare className="h-8 w-8 text-primary" />
      </div>
      
      <h2 className="mb-2 text-xl font-semibold text-foreground">
        How can I help you today?
      </h2>
      <p className="mb-8 max-w-md text-center text-sm text-muted-foreground">
        Ask me anything about your documents. I'll search through your knowledge base to find the most relevant information.
      </p>

      <div className="grid max-w-lg gap-3 sm:grid-cols-2">
        <div className="flex items-start gap-3 rounded-xl border border-border bg-card/50 p-4 transition-colors hover:bg-card">
          <Sparkles className="h-5 w-5 shrink-0 text-primary" />
          <div>
            <p className="text-sm font-medium text-foreground">Smart Retrieval</p>
            <p className="text-xs text-muted-foreground">
              Uses AI to find the most relevant context
            </p>
          </div>
        </div>

        <div className="flex items-start gap-3 rounded-xl border border-border bg-card/50 p-4 transition-colors hover:bg-card">
          <BookOpen className="h-5 w-5 shrink-0 text-primary" />
          <div>
            <p className="text-sm font-medium text-foreground">Document-Based</p>
            <p className="text-xs text-muted-foreground">
              Answers grounded in your knowledge base
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmptyState;
