from Stream_AutoExpiryExtendSessionManager import SessionManager
import time

manager = SessionManager()

user_id = "user_101"

# First Message
session_id = manager.handle_message(
    user_id=user_id,
    message="Tell me about unlimited data plans"
)

print(f"\nSession ID: {session_id}")
print(f"TTL After Message 1: {manager.get_ttl(user_id)}")

# Wait 20 Seconds
print("\nWaiting 20 seconds...\n")
time.sleep(20)

print(f"TTL Before Message 2: {manager.get_ttl(user_id)}")

# Second Message
session_id = manager.handle_message(
    user_id=user_id,
    message="Set DND on my number"
)

print(f"\nSession ID: {session_id}")
print(f"TTL After Message 2: {manager.get_ttl(user_id)}")

print("\n===== SESSION DATA =====")

session_data = manager.get_session(user_id)

if session_data:
    for entry_id, data in session_data:
        print(entry_id, data)

print(f"\nFinal TTL: {manager.get_ttl(user_id)}")
