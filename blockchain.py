import hashlib
import datetime


# Block class to represent a block in the blockchain
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(data_string.encode()).hexdigest()


# Blockchain class to manage the blocks
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

# Project class to represent a project
class Project:
    def __init__(self, title):
        self.title = title

    def calculate_hash(self):
        data_string = self.title
        return hashlib.sha256(data_string.encode()).hexdigest()

# Function to verify the authenticity of a project
def verify_project(project, blockchain):
    project_hash = project.calculate_hash()
    for block in blockchain.chain:
        if project_hash == block.data:
            print("Project is authentic.")
            return "Authentic"
    print("Project is suspicious or potentially fake.")
    return "Suspicious or Fake"

# Create a blockchain
# blockchain = Blockchain()
#
# # Create some projects
# project1 = Project("Project 1")
# project2 = Project("Project 2")
# project3 = Project("Project 3")
#
# # Add projects to the blockchain
# blockchain.add_block(Block(1, datetime.datetime.now(), project1.calculate_hash(), ""))
# blockchain.add_block(Block(2, datetime.datetime.now(), project2.calculate_hash(), ""))
#
# # Verify project authenticity
# verify_project(project1, blockchain)
# verify_project(project2, blockchain)
# verify_project(project3, blockchain)
