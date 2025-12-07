import { useState, useEffect } from "react";
import { Settings, X, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ChatSettings, getSettings, saveSettings } from "@/lib/chatApi";
import { toast } from "@/hooks/use-toast";

interface SettingsPanelProps {
  onSettingsChange: (settings: ChatSettings) => void;
}

const SettingsPanel = ({ onSettingsChange }: SettingsPanelProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [settings, setSettings] = useState<ChatSettings>(getSettings);

  useEffect(() => {
    onSettingsChange(settings);
  }, []);

  const handleSave = () => {
    saveSettings(settings);
    onSettingsChange(settings);
    setIsOpen(false);
    toast({
      title: "Settings saved",
      description: "Your API settings have been saved.",
    });
  };

  return (
    <>
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setIsOpen(true)}
        className="h-9 w-9 text-muted-foreground hover:text-foreground hover:bg-muted"
      >
        <Settings className="h-5 w-5" />
      </Button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-background/80 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
          />

          <div className="glass-effect relative z-10 w-full max-w-md rounded-xl border border-border p-6 shadow-2xl">
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-foreground">Settings</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsOpen(false)}
                className="h-8 w-8 text-muted-foreground hover:text-foreground"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="baseUrl" className="text-sm text-foreground">
                  API Base URL
                </Label>
                <Input
                  id="baseUrl"
                  value={settings.baseUrl}
                  onChange={(e) =>
                    setSettings({ ...settings, baseUrl: e.target.value })
                  }
                  placeholder="http://localhost:5000"
                  className="bg-input border-border text-foreground placeholder:text-muted-foreground focus:border-primary focus:ring-primary"
                />
                <p className="text-xs text-muted-foreground">
                  Enter your Flask API URL (e.g., ngrok URL)
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="topK" className="text-sm text-foreground">
                  Top K (Retrieved Documents)
                </Label>
                <Input
                  id="topK"
                  type="number"
                  min={1}
                  max={10}
                  value={settings.topK}
                  onChange={(e) =>
                    setSettings({ ...settings, topK: parseInt(e.target.value) || 3 })
                  }
                  className="bg-input border-border text-foreground focus:border-primary focus:ring-primary"
                />
                <p className="text-xs text-muted-foreground">
                  Number of relevant documents to retrieve (1-10)
                </p>
              </div>
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <Button
                variant="ghost"
                onClick={() => setIsOpen(false)}
                className="text-muted-foreground hover:text-foreground"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSave}
                className="bg-primary text-primary-foreground hover:bg-primary/90 glow-primary"
              >
                <Save className="mr-2 h-4 w-4" />
                Save Settings
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default SettingsPanel;
