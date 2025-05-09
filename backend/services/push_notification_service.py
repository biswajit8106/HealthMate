import json
from pywebpush import webpush, WebPushException
from models.push_subscription_model import PushSubscription
from database.db import SessionLocal

VAPID_PRIVATE_KEY = "S5O1LVd62eyZDaQ-Xk3Q-N-PBAAcJKmvSTgMRmczWXA"
VAPID_CLAIMS = {
    "sub": "mailto:your-email@example.com"
}

def send_push_notification(user_id, payload):
    db = SessionLocal()
    try:
        subscription = db.query(PushSubscription).filter_by(user_id=user_id).first()
        if not subscription:
            print(f"No push subscription found for user {user_id}")
            return False

        subscription_info = json.loads(subscription.subscription_info)
        try:
            webpush(
                subscription_info,
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            print(f"Push notification sent to user {user_id}")
            return True
        except WebPushException as ex:
            print(f"WebPush error: {ex}")
            return False
    except Exception as e:
        print(f"Unexpected error in send_push_notification: {e}")
        return False
    finally:
        db.close()
