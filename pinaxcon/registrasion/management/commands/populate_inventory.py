from collections import namedtuple
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from registrasion.models import inventory as inv
from registrasion.models import conditions as cond
from symposion import proposals

class Command(BaseCommand):
    help = 'Populates the inventory with the LCA2017 inventory model'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        kinds = []
        kinds.append(proposals.models.ProposalKind.objects.get(name="talk"))
        self.main_conference_proposals = kinds

        self.populate_groups()
        self.populate_inventory()
        self.populate_restrictions()
        self.populate_discounts()

    def populate_groups(self):
        self.group_team = self.find_or_make(
            Group,
            ("name", ),
            name="Conference organisers",
        )
        self.group_volunteers = self.find_or_make(
            Group,
            ("name", ),
            name="Conference volunteers",
        )
        self.group_unpublish = self.find_or_make(
            Group,
            ("name", ),
            name="Can see unpublished products",
        )

    def populate_inventory(self):
        # Categories

        self.ticket = self.find_or_make(
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

        self.ticket_fairy = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Fairy Penguin Sponsor",
            price=Decimal("1999.00"),
            reservation_duration=hours(24),
            order=1,
        )
        self.ticket_professional = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Professional",
            price=Decimal("999.00"),
            reservation_duration=hours(24),
            order=10,
        )
        self.ticket_hobbyist = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Hobbyist",
            price=Decimal("449.00"),
            reservation_duration=hours(24),
            order=20,
        )
        self.ticket_student = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Student",
            price=Decimal("160.00"),
            reservation_duration=hours(24),
            order=30,
        )
        self.ticket_miniconfs_mt = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Monday and Tuesday Only",
            price=Decimal("198.00"),
            reservation_duration=hours(24),
            order=40,
        )
        self.ticket_miniconfs_mon = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Monday Only",
            price=Decimal("99.00"),
            reservation_duration=hours(24),
            order=42,
        )
        self.ticket_miniconfs_tue = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Tuesday Only",
            price=Decimal("99.00"),
            reservation_duration=hours(24),
            order=44,
        )
        self.ticket_speaker = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Speaker",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=50,
        )
        self.ticket_media = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Media",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=60,
        )
        self.ticket_sponsor = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Sponsor",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=70,
        )
        self.ticket_team = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Conference Organiser",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=80,
        )
        self.ticket_volunteer = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.ticket,
            name="Conference Volunteer",
            price=Decimal("00.00"),
            reservation_duration=hours(24),
            order=90,
        )

        # Penguin dinner

        self.penguin_adult = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.penguin_dinner,
            name="Adult",
            description="Includes an adult's meal and full beverage service.",
            price=Decimal("95.00"),
            reservation_duration=hours(1),
            order=10,
        )
        self.penguin_child = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.penguin_dinner,
            name="Child",
            description="Includes a child's meal and soft drink service.",
            price=Decimal("50.00"),
            reservation_duration=hours(1),
            order=20,
        )
        self.penguin_infant = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.penguin_dinner,
            name="Infant",
            description="Includes no food or beverage service.",
            price=Decimal("00.00"),
            reservation_duration=hours(1),
            order=30,
        )

        # Speakers' dinner

        self.speakers_adult = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.speakers_dinner_ticket,
            name="Adult",
            description="Includes an adult's meal and full beverage service.",
            price=Decimal("100.00"),
            reservation_duration=hours(1),
            order=10,
        )
        self.speakers_child = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.speakers_dinner_ticket,
            name="Child",
            description="Includes a child's meal and soft drink service.",
            price=Decimal("60.00"),
            reservation_duration=hours(1),
            order=20,
        )
        self.speaker_infant = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.speakers_dinner_ticket,
            name="Infant",
            description="Infant must be seated in an adult's lap. No food or "
                        "beverage service.",
            price=Decimal("00.00"),
            reservation_duration=hours(1),
            order=30,
        )

        # PDNS breakfast

        self.pdns = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.pdns_breakfast,
            name="Conference Attendee",
            price=Decimal("00.00"),
            reservation_duration=hours(1),
            limit_per_user=1,
            order=10,
        )

        # Accommodation

        self.accommodation_week = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.accommodation,
            name="Single Bedroom with Shared Bathrooms, includes full "
                 "breakfast, Sunday 15 January 2017--Saturday 21 January 2017",
            price=Decimal("396.00"),
            reservation_duration=hours(24),
            limit_per_user=1,
            order=10,
        )

        # Extras

        self.carbon_offset = self.find_or_make(
            inv.Product,
            ("name", "category",),
            category=self.extras,
            name="Offset the carbon polution generated by your attendance, "
                 "thanks to fifteen trees.",
            price=Decimal("5.00"),
            reservation_duration=hours(1),
            order=10,
        )

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
        order = 0
        for name, group in shirt_names.items():
            self.shirts[name] = {}
            prefix = group.prefix
            for size in group.sizes:
                product_name = "%s %s" % (prefix, size)
                order += 10
                self.shirts[name][size] = self.find_or_make(
                    inv.Product,
                    ("name", "category",),
                    name=product_name,
                    category=self.t_shirt,
                    price=Decimal("25.00"),
                    reservation_duration=hours(1),
                    order=order,
                )

    def populate_restrictions(self):

        # Hide the products that will eventually need a voucher
        hide_voucher_products = self.find_or_make(
            cond.GroupMemberFlag,
            ("description", ),
            description="Can see hidden products",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )
        hide_voucher_products.group.set([self.group_unpublish])
        hide_voucher_products.products.set([
            self.ticket_media,
            self.ticket_sponsor,
        ])

        # Volunteer tickets are for volunteers only
        volunteers = self.find_or_make(
            cond.GroupMemberFlag,
            ("description", ),
            description="Volunteer tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )
        volunteers.group.set([self.group_volunteers])
        volunteers.products.set([
            self.ticket_volunteer,
        ])

        # Team tickets are for team members only
        team = self.find_or_make(
            cond.GroupMemberFlag,
            ("description", ),
            description="Team tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )
        team.group.set([self.group_team])
        team.products.set([
            self.ticket_team,
        ])

        # Speaker tickets are for primary speakers only
        speaker_tickets = self.find_or_make(
            cond.SpeakerFlag,
            ("description", ),
            description="Speaker tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
            is_presenter=True,
            is_copresenter=False,
        )
        speaker_tickets.proposal_kind.set(self.main_conference_proposals)
        speaker_tickets.products.set([self.ticket_speaker, ])

        # Speaker dinner tickets are for primary and secondary speakers
        speaker_dinner_tickets = self.find_or_make(
            cond.SpeakerFlag,
            ("description", ),
            description="Speaker dinner tickets",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
            is_presenter=True,
            is_copresenter=True,
        )
        speaker_dinner_tickets.proposal_kind.set([])
        speaker_dinner_tickets.categories.set([self.speakers_dinner_ticket, ])

        # PDNS tickets are complicated.
        # They can be enabled by tickets
        pdns_by_ticket = self.find_or_make(
            cond.ProductFlag,
            ("description", ),
            description="PDNS available by ticket",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
        )
        pdns_by_ticket.enabling_products.set([
            self.ticket_professional,
            self.ticket_fairy,
            self.ticket_media,
            self.ticket_sponsor,
        ])
        pdns_by_ticket.categories.set([self.pdns_breakfast, ])

        # They are available to speakers
        pdns_by_speaker = self.find_or_make(
            cond.SpeakerFlag,
            ("description", ),
            description="PDNS available to speakers",
            condition=cond.FlagBase.ENABLE_IF_TRUE,
            is_presenter=True,
            is_copresenter=True,

        )
        pdns_by_speaker.proposal_kind.set(self.main_conference_proposals)
        pdns_by_speaker.categories.set([self.pdns_breakfast, ])

        # They are available to staff
        pdns_by_staff = self.find_or_make(
            cond.GroupMemberFlag,
            ("description", ),
            description="PDNS available to staff",
            condition=cond.FlagBase.ENABLE_IF_TRUE,

        )
        pdns_by_staff.group.set([
            self.group_team,
            self.group_volunteers,
        ])
        pdns_by_staff.categories.set([self.pdns_breakfast, ])

    def populate_discounts(self):

        def add_early_birds(discount):
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_fairy,
                price=Decimal("200.00"),
                quantity=1,  # Per user
            )
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_professional,
                price=Decimal("200.00"),
                quantity=1,  # Per user
            )
            self.find_or_make(
                cond.DiscountForProduct,
                ("discount", "product"),
                discount=discount,
                product=self.ticket_hobbyist,
                price=Decimal("150.00"),
                quantity=1,  # Per user
            )

        def free_category(parent_discount, category, quantity=1):
            self.find_or_make(
                cond.DiscountForCategory,
                ("discount", "category",),
                discount=parent_discount,
                category=category,
                percentage=Decimal("100.00"),
                quantity=quantity,
            )

        # Early Bird Discount (general public)
        early_bird = self.find_or_make(
            cond.TimeOrStockLimitDiscount,
            ("description", ),
            description="Early Bird",
            end_time=datetime(year=2016, month=11, day=1),
            limit=165,  # Across all users
        )
        add_early_birds(early_bird)

        # Early bird rates for speakers
        speaker_ticket_discounts = self.find_or_make(
            cond.SpeakerDiscount,
            ("description", ),
            description="Speaker Ticket Discount",
            is_presenter=True,
            is_copresenter=True,
        )
        speaker_ticket_discounts.proposal_kind.set(
            self.main_conference_proposals,
        )
        add_early_birds(speaker_ticket_discounts)

        # Primary speaker gets a free speaker dinner ticket
        primary_speaker = self.find_or_make(
            cond.SpeakerDiscount,
            ("description", ),
            description="Primary Speaker",
            is_presenter=True,
            is_copresenter=False,
        )
        free_category(primary_speaker, self.speakers_dinner_ticket)

        # Professional-Like ticket inclusions
        ticket_prolike_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Included with Professional ticket",
        )
        ticket_prolike_inclusions.enabling_products.set([
            self.ticket_fairy,
            self.ticket_professional,
            self.ticket_media,
            self.ticket_sponsor,
            self.ticket_speaker,
        ])
        free_category(ticket_prolike_inclusions, self.penguin_dinner)
        free_category(ticket_prolike_inclusions, self.t_shirt)

        # Hobbyist ticket inclusions
        ticket_hobbyist_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Included with Hobbyist ticket",
        )
        ticket_hobbyist_inclusions.enabling_products.set([
            self.ticket_hobbyist,
        ])
        free_category(ticket_hobbyist_inclusions, self.t_shirt)

        # Student ticket inclusions
        ticket_student_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Included with Student ticket",
        )
        ticket_student_inclusions.enabling_products.set([
            self.ticket_student,
        ])
        free_category(ticket_student_inclusions, self.t_shirt)

        # Team & volunteer ticket inclusions
        ticket_staff_inclusions = self.find_or_make(
            cond.IncludedProductDiscount,
            ("description", ),
            description="Included with staff ticket",
        )
        ticket_staff_inclusions.enabling_products.set([
            self.ticket_team,
            self.ticket_volunteer,
        ])
        free_category(ticket_staff_inclusions, self.penguin_dinner)

        # Team & volunteer t-shirts, regardless of ticket type
        staff_t_shirts = self.find_or_make(
            cond.GroupMemberDiscount,
            ("description", ),
            description="Staff t-shirt",
        )
        staff_t_shirts.group.set([
            self.group_team,
            self.group_volunteers,
        ])
        free_category(staff_t_shirts, self.t_shirt, quantity=5)

    def find_or_make(self, model, search_keys, **k):
        ''' Either makes or finds an object of type _model_, with the given
        kwargs.

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


def hours(n):
    return timedelta(hours=n)
