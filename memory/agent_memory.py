# memory/agent_memory.py

class AgentMemory:
    """
    Simple in-memory storage for agent state
    """

    def __init__(self):
        self.memory = {}

    def save(self, key, value):
        """
        Save a value in memory with the given key
        """
        self.memory[key] = value

    def load(self, key):
        """
        Retrieve a value from memory by key
        """
        return self.memory.get(key, None)

    def get_memory(self):
        """
        Return a snapshot of the current memory (for LLM reasoning)
        """
        return {k: str(v) for k, v in self.memory.items()}

    def clear(self):
        """
        Clear all stored memory
        """
        self.memory = {}
