"""SMS to trusted contacts. Simulated (logged) unless Twilio env vars are set."""
import logging
from typing import List, Tuple
from app import config

log = logging.getLogger("notify")


def send_sms(to: str, body: str) -> bool:
    if config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN and config.TWILIO_FROM_NUMBER:
        try:
            from twilio.rest import Client  # pip install twilio
            Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN).messages.create(
                to=to, from_=config.TWILIO_FROM_NUMBER, body=body)
            return True
        except Exception as exc:
            log.error("SMS failed to %s: %s", to, exc)
            return False
    log.info("[SIMULATED SMS] to=%s body=%s", to, body)
    return True


def notify_each(items: List[Tuple[str, str]]) -> int:
    """items = [(phone, body), ...] -> number delivered."""
    return sum(1 for phone, body in items if send_sms(phone, body))
