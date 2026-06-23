import json
import os
from memory_sleuth import MemorySleuth

def test_start_setup_wizard():
    memory_sleuth = MemorySleuth()
    progress = memory_sleuth.start_setup_wizard()
    assert progress['step'] == 1

def test_install_agent():
    memory_sleuth = MemorySleuth()
    memory_sleuth.start_setup_wizard()
    progress = memory_sleuth.install_agent('api_key')
    assert progress['agent_installed'] == True
    assert progress['api_key'] == 'api_key'

def test_generate_api_key():
    memory_sleuth = MemorySleuth()
    api_key = memory_sleuth.generate_api_key()
    assert api_key == 'generated_api_key'

def test_select_feature_flags():
    memory_sleuth = MemorySleuth()
    memory_sleuth.start_setup_wizard()
    progress = memory_sleuth.select_feature_flags(['flag1', 'flag2'])
    assert progress['feature_flags'] == ['flag1', 'flag2']

def test_save_progress():
    memory_sleuth = MemorySleuth()
    memory_sleuth.start_setup_wizard()
    memory_sleuth.install_agent('api_key')
    memory_sleuth.select_feature_flags(['flag1', 'flag2'])
    memory_sleuth.save_progress()
    with open('progress.json', 'r') as f:
        progress = json.load(f)
    assert progress['step'] == 1
    assert progress['agent_installed'] == True
    assert progress['api_key'] == 'api_key'
    assert progress['feature_flags'] == ['flag1', 'flag2']

def test_load_progress():
    # Clean up any existing state from previous tests to ensure isolation
    if os.path.exists('progress.json'):
        os.remove('progress.json')

    memory_sleuth = MemorySleuth()
    memory_sleuth.load_progress()
    assert memory_sleuth.progress == {}

def test_complete_setup_wizard():
    memory_sleuth = MemorySleuth()
    memory_sleuth.start_setup_wizard()
    memory_sleuth.install_agent('api_key')
    memory_sleuth.select_feature_flags(['flag1', 'flag2'])
    assert memory_sleuth.complete_setup_wizard() == True

def test_send_welcome_email():
    memory_sleuth = MemorySleuth()
    memory_sleuth.start_setup_wizard()
    memory_sleuth.install_agent('api_key')
    memory_sleuth.select_feature_flags(['flag1', 'flag2'])
    assert memory_sleuth.send_welcome_email() == 'Welcome email sent'

def test_send_welcome_email_not_completed():
    memory_sleuth = MemorySleuth()
    assert memory_sleuth.send_welcome_email() == 'Setup wizard not completed'
