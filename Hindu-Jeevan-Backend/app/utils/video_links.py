import uuid

def generate_jitsi_link(client_name: str):
    room_name = f"HinduJeevanGyaan_{client_name}_{uuid.uuid4().hex[:6]}"
    return f"https://meet.jit.si/{room_name}"
