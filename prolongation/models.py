from django.db import models


class ProlongedTicket(models.Model):
    class Name(models.TextChoices):
        PAYMENT_CALL = 'Wezwanie do zapłaty'
        BLANKET = 'Blankietowy'
        REPLACEMENT = 'Zastępczy'

    name = models.CharField('Nazwa', choices=Name.choices, max_length=128, unique=True)

    class Meta:
        verbose_name = 'Prologowany Bilet'
        verbose_name_plural = 'Prolongowane Bilety'


class TicketProlongation(models.Model):
    expires_at = models.DateField(verbose_name='Data wygaśnięcia')

    class TicketName(models.TextChoices):
        PAYMENT_CALL = 'Wezwanie do zapłaty'
        BLANKET = 'Bilet blankietowy'

    ticket_name = models.CharField('Nazwa biletu', max_length=128)

    class Meta:
        verbose_name = 'Dokument'
        verbose_name_plural = 'Dokumenty'
