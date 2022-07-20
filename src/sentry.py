import sentry_sdk

from .config import SENTRY_DSN

def init_sentry(rate: float=1.0) -> None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=rate,
    )
