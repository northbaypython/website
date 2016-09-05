from collections import namedtuple
from django.core.exceptions import DoesNotExist
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Populates the inventory with the LCA2017 inventory model'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        self.populate_inventory()
        self.populate_discounts()

    def populate_inventory(self):
        # Categories

        self.tickets = None
        self.penguin_dinner = None
        self.speakers_dinner_ticket = None
        self.pdns_breakfast = None
        self.t_shirt = None
        self.accommodation = None
        self.extras = None

        # Tickets

        self.ticket_fairy = None
        self.ticket_professional = None
        self.ticket_hobbyist = None
        self.ticket_student = None
        self.ticket_miniconfs_mt = None
        self.ticket_miniconfs_mon = None
        self.ticket_miniconfs_tue = None
        self.ticket_speaker = None
        self.ticket_media = None
        self.ticket_sponsor = None
        self.ticket_team = None
        self.ticket_volunteer = None

        # Penguin dinner

        self.penguin_adult = None
        self.penguin_child = None
        self.penguin_infant = None

        # Speakers' dinner

        self.speakers_adult = None
        self.speakers_child = None
        self.speaker_infant = None

        # PDNS breakfast

        self.pdns = None

        # Accommodation

        self.accommodation_week = None

        # Extras

        self.carbon_offset = None

        # Shirts
        ShirtGroup = namedtuple("ShirtGroup", ("prefix", "sizes"))
        shirt_names = {
            "mens": ShirtGroup(
                "Men's/Straight Cut Size",
                ("S", "M", "L", "XL", "2XL", "3XL", "5XL"),
            ),
            "womens_classic": ShirtGroup(
                "Women's Classic Fit",
                ("XS", "S", "M", "L", "XL", "2XL"),
            ),
            "womens_semi": ShirtGroup(
                "Women's Semi-Fitted",
                ("S", "M", "L", "XL", "2XL"),
            ),
        }

        self.shirts = {}
        for name, group in shirt_names.items():
            self.shirts[name] = {}
            prefix = group.prefix
            for size in group.sizes:
                product_name = "%s %s" % (prefix, size)
                self.shirts[name][size] = None

    def populate_discounts(self):
        pass


def find_or_make(model, **k):
    ''' Either makes or finds an object of type _model_, with the given kwargs
    '''

    try:
        return model.objects.get(**k)
    except DoesNotExist:
        return model.objects.create(**k)
