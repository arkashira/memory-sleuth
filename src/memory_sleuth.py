import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AgentInstallation:
    api_key: str
    feature_flags: List[str]

class MemorySleuth:
    def __init__(self):
        self.progress = {}

    def start_setup_wizard(self):
        self.progress['step'] = 1
        return self.progress

    def install_agent(self, api_key: str):
        self.progress['agent_installed'] = True
        self.progress['api_key'] = api_key
        return self.progress

    def generate_api_key(self):
        return 'generated_api_key'

    def select_feature_flags(self, feature_flags: List[str]):
        self.progress['feature_flags'] = feature_flags
        return self.progress

    def save_progress(self):
        with open('progress.json', 'w') as f:
            json.dump(self.progress, f)

    def load_progress(self):
        try:
            with open('progress.json', 'r') as f:
                self.progress = json.load(f)
        except FileNotFoundError:
            pass

    def complete_setup_wizard(self):
        if 'agent_installed' in self.progress and 'api_key' in self.progress and 'feature_flags' in self.progress:
            return True
        return False

    def send_welcome_email(self):
        if self.complete_setup_wizard():
            return 'Welcome email sent'
        return 'Setup wizard not completed'

def main():
    memory_sleuth = MemorySleuth()
    memory_sleuth.start_setup_wizard()
    memory_sleuth.install_agent(memory_sleuth.generate_api_key())
    memory_sleuth.select_feature_flags(['flag1', 'flag2'])
    memory_sleuth.save_progress()
    print(memory_sleuth.send_welcome_email())

if __name__ == '__main__':
    main()
