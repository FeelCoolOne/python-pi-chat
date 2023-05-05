from heypi.conversation import Conversation

class Client:
    
    def create_conversation(self):
        return Conversation()

    def resume_conversation(self, identifiers):
        return Conversation(identifiers)
