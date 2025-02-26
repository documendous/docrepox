import logging

from django.conf import settings

from apps.dashlets.models import Motd


def get_motd():  # pragma: no coverage
    log = logging.getLogger(__name__)
    motd = None
    use_motd = False

    if hasattr(settings, "USE_MOTD") and settings.USE_MOTD:
        log.debug("MOTD dashlet enabled. Using MOTD dashlet.")
        use_motd = settings.USE_MOTD

        try:
            motd = Motd.objects.filter(is_published=True)[0]
        except IndexError:
            motd = Motd.objects.none()

    else:
        log.debug("MOTD dashlet disabled. Not using MOTD.")

    return use_motd, motd
