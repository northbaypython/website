from collections import namedtuple
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from registrasion.models import inventory as inv

class Command(BaseCommand):
    help = 'Populates the inventory with the LCA2017 inventory model'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.populate_inventory()
        self.populate_discounts()

    def populate_inventory(self):
        # Categories

        self.tickets = self.find_or_make(
            inv.Category,
            ("name",),
            name="Ticket",
            description="Each type of ticket has different included products. "
                        "For details of what products are included, see our "
                        "[LINK]registration details page.[/LINK]",
            required = True,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=1,
            order=1,
        )
        self.penguin_dinner = self.find_or_make(
            inv.Category,
            ("name",),
            name="Penguin Dinner Ticket",
            description="Tickets to our conference dinner on the evening of "
                        "Wednesday 18 January. All attendees may purchase "
                        "seats at the dinner, even if a dinner ticket is not "
                        "included in your conference ticket price.",
            required = False,
            render_type=inv.Category.RENDER_TYPE_QUANTITY,
            limit_per_user=10,
            order=10,
        )
        self.speakers_dinner_ticket = self.find_or_make(
            inv.Category,
            ("name",),
            name="Speakers' Dinner Ticket",
            description="Tickets to our exclusive Speakers' Dinner on the "
                        "evening of Tuesday 17 January. You may purchase up "
                        "to 5 tickets in total, for significant others, and "
                        "family members.",
            required = False,
            render_type=inv.Category.RENDER_TYPE_QUANTITY,
            limit_per_user=5,
            order=20,
        )
        self.pdns_breakfast = self.find_or_make(
            inv.Category,
            ("name",),
            name="Opening Reception Breakfast Ticket",
            description="Tickets to our Opening Reception Breakfast. This "
                        "event will be held on the morning of Monday 16 "
                        "January, and is restricted to Professional Ticket "
                        "holders, speakers, miniconf organisers, and invited "
                        "guests.",
            required = False,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=1,
            order=30,
        )
        self.t_shirt = self.find_or_make(
            inv.Category,
            ("name",),
            name="T-Shirt",
            description="Commemorative conference t-shirts, featuring secret "
                        "linux.conf.au 2017 artwork.",
            required = False,
            render_type=inv.Category.RENDER_TYPE_ITEM_QUANTITY,
            order=40,
        )
        self.accommodation = self.find_or_make(
            inv.Category,
            ("name",),
            name="Accommodation at University of Tasmania",
            description="Accommodation at the University of Tasmania colleges "
                        "and apartments. You can come back and book your "
                        "accommodation at a later date, provided rooms remain "
                        "available. Rooms may only be booked from Sunday 15 "
                        "January--Saturday 21 January. If you wish to stay "
                        "for only a part of the 6-day period, you must book "
                        "accommodation for the full 6-day period. Rooms at "
                        "other hotels, including Wrest Point can be booked "
                        "elsewhere. For full details, see [LINK]our "
                        "accommodation page.[/LINK]",
            required = False,
            render_type=inv.Category.RENDER_TYPE_RADIO,
            limit_per_user=1,
            order=50,
        )
        self.extras = self.find_or_make(
            inv.Category,
            ("name",),
            name="Extras",
            description="Other items that can improve your conference "
                        "experience.",
            required = False,
            render_type=inv.Category.RENDER_TYPE_QUANTITY,
            order=60,
        )

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


    def find_or_make(self, model, search_keys, **k):
        ''' Either makes or finds an object of type _model_, with the given kwargs.

        Arguments:
            search_keys ([str, ...]): A sequence of keys that are used to search
            for an existing version in the database. The remaining arguments are
            only used when creating a new object.
        '''

        try:
            keys = dict((key, k[key]) for key in search_keys)
            a = model.objects.get(**keys)
            self.stdout.write("FOUND  : " + str(keys))
            model.objects.filter(id=a.id).update(**k)
            a.refresh_from_db()
            return a
        except ObjectDoesNotExist:
            a = model.objects.create(**k)
            self.stdout.write("CREATED: " + str(k))
            return a
