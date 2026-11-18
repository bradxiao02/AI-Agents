import sys
from pathlib import Path

# Allow Python to import files from src.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import agent


# ==========================================
# TEST SAVING AND LOADING MEMORY
# ==========================================

def test_save_and_load_memory(tmp_path, monkeypatch):

    # Use a temporary file instead of the real conversation history.
    test_file = tmp_path / "conversation_history.json"

    monkeypatch.setattr(agent, "MEMORY_FILE", test_file)

    history = [
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": "Hello! How can I help?"
        }
    ]

    agent.save_memory(history)

    loaded_history = agent.load_memory()

    assert loaded_history == history


# ==========================================
# TEST EMPTY MEMORY
# ==========================================

def test_load_memory_when_file_does_not_exist(tmp_path, monkeypatch):

    test_file = tmp_path / "missing_history.json"

    monkeypatch.setattr(agent, "MEMORY_FILE", test_file)

    result = agent.load_memory()

    assert result == []


# ==========================================
# TEST CLEARING MEMORY
# ==========================================

def test_clear_history(tmp_path, monkeypatch):

    test_file = tmp_path / "conversation_history.json"

    monkeypatch.setattr(agent, "MEMORY_FILE", test_file)

    history = [
        {
            "role": "user",
            "content": "Remember this message"
        }
    ]

    agent.save_memory(history)

    result = agent.clear_history()

    assert result == []
    assert agent.load_memory() == []


# ==========================================
# TEST RECENT CONVERSATION HISTORY
# ==========================================

def test_get_recent_history():

    history = [
        {"role": "user", "content": "Message 1"},
        {"role": "assistant", "content": "Reply 1"},
        {"role": "user", "content": "Message 2"},
        {"role": "assistant", "content": "Reply 2"},
        {"role": "user", "content": "Message 3"},
        {"role": "assistant", "content": "Reply 3"}
    ]

    result = agent.get_recent_history(history, max_turns=2)

    assert len(result) == 4
    assert result[-1]["content"] == "Reply 3"