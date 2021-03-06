# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_conferencespeaker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talkproposal',
            name='audience_level',
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='extended_presentation',
            field=models.BooleanField(default=False, help_text='Most talks at North Bay Python go for 30 minutes. We have some openings for 45-minute talks. If you check this field, please explain in your additional notes how you would use the extra 15 minutes.', verbose_name='Optionally consider this proposal for a 45-minute slot'),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='extra_av',
            field=models.TextField(blank=True, help_text='We will provide you with a projector with HDMI connection, an audio connection, and one microphone per speaker. If you need anything more than this to present this talk, please list them here.', verbose_name='Extra tech and A/V requirements'),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='new_presentation',
            field=models.BooleanField(default=False, help_text='Check this box if North Bay Python will be the first time this talk is presented at a technical conference.', verbose_name='This is a new presentation'),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='slides_release',
            field=models.BooleanField(default=True, help_text='I authorize North Bay Python to release a copy of my slides and related materials under the Creative Commons Attribution-ShareAlike 3.0 United States licence, and certify that I have the authority to do so.'),
        ),
        migrations.AlterField(
            model_name='conferencespeaker',
            name='experience',
            field=models.TextField(blank=True, help_text="List any past speaking experience you have. This can include user groups, meetups, or presentations at work or school.  Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/target='_blank'>Markdown</a>.", verbose_name='Past speaking experience'),
        ),
        migrations.AlterField(
            model_name='conferencespeaker',
            name='first_time',
            field=models.BooleanField(help_text='Check this field if this is your first time speaking at a technical conference.', verbose_name='First-time speaker?'),
        ),
        migrations.AlterField(
            model_name='conferencespeaker',
            name='lodging_assistance',
            field=models.BooleanField(help_text='Check this field if you require lodging assistance in Petaluma, California during North Bay Python.', verbose_name='Lodging assistance required?'),
        ),
        migrations.AlterField(
            model_name='conferencespeaker',
            name='minority_group',
            field=models.CharField(blank=True, help_text='If you are a member of one or more groups that are under-represented in the tech industry, you may list these here. Your response is optional.', max_length=256, verbose_name='Diversity statement'),
        ),
        migrations.AlterField(
            model_name='conferencespeaker',
            name='travel_assistance',
            field=models.BooleanField(help_text='Check this field if you require travel assistance to get to North Bay Python in Petaluma, California.', verbose_name='Travel assistance required?'),
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text='I authorize North Bay Python to release a recording of my talk under the Creative Commons Attribution-ShareAlike 3.0 United States licence.'),
        ),
    ]
