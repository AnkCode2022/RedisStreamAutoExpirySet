import redis
import uuid
from datetime import datetime, timedelta


class SessionManager:

    SESSION_TTL = 60  # 60 seconds for testing

    def __init__(self, host="localhost", port=6379):
        self.redis = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )

    def _stream_key(self, user_id: str) -> str:
        return f"user_session:{user_id}"

    def handle_message(self, user_id: str, message: str) -> str:

        key = self._stream_key(user_id)

        last_updated_time = datetime.utcnow().isoformat()

        expiry_time = (
            datetime.utcnow() +
            timedelta(seconds=self.SESSION_TTL)
        ).isoformat()

        # Existing Session
        if self.redis.exists(key):
            first_entry = self.redis.xrange(key, count=1)
            session_id = first_entry[0][1]["session_id"]

        # New Session
        else:
            session_id = str(uuid.uuid4())

            self.redis.xadd(
                key,
                {
                    "event": "session_created",
                    "session_id": session_id,
                    "message": "SESSION_STARTED",
                    "last_updated_time": last_updated_time,
                    "expiry_time": expiry_time
                }
            )

        # Store User Message
        self.redis.xadd(
            key,
            {
                "event": "message",
                "session_id": session_id,
                "message": message,
                "last_updated_time": last_updated_time,
                "expiry_time": expiry_time
            }
        )

        # Refresh Session Expiry
        self.redis.expire(key, self.SESSION_TTL)

        return session_id

    def get_session(self, user_id: str):

        key = self._stream_key(user_id)

        if not self.redis.exists(key):
            return None

        return self.redis.xrange(key)

    def get_ttl(self, user_id: str):

        key = self._stream_key(user_id)

        if not self.redis.exists(key):
            return -1

        return self.redis.ttl(key)

    def delete_session(self, user_id: str):
        self.redis.delete(self._stream_key(user_id))
