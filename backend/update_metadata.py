import os

time = 0
metadata_list = []
def create_metadata():
    global time
    causal_metadata = f"{os.environ.get('SOCKET_ADDRESS')}-{str(time)}"
    time += 1
    return causal_metadata

def check_metadata(metadata):
    if metadata in metadata_list or metadata == "null" or metadata == None:
        return True
    elif metadata not in metadata_list:
        return False
    
def update_metadata(metadata):
    metadata_list.append(metadata)

def print_metadata():
    print(metadata_list)