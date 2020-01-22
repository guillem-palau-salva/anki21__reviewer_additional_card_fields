import os
import pathlib

from anki import version as anki_version
from anki.hooks import addHook
from aqt import mw
from aqt.utils import askUser

newold = {
    "{{info::FirstReview}}": "{{info-FirstReview:}}",
    "{{info::LastReview}}": "{{info-LastReview:}}",
    "{{info::TimeAvg}}": "{{info-TimeAvg:}}",
    "{{info::TimeTotal}}": "{{info-TimeTotal:}}",
    "{{info::overdue_fmt}}": "{{info-overdue_fmt:}}",
    "{{info::overdue_days}}": "{{info-overdue_days:}}",
    "{{info::external_file_link}}": "{{info-external_file_link:}}",
    "{{info::Ord}}": "{{info-Ord:}}",
    "{{info::Did}}": "{{info-Did:}}",
    "{{info::Due}}": "{{info-Due:}}",
    "{{info::Id}}": "{{info-Id:}}",
    "{{info::Ivl}}": "{{info-Ivl:}}",
    "{{info::Queue}}": "{{info-Queue:}}",
    "{{info::Reviews}}": "{{info-Reviews:}}",
    "{{info::Lapses}}": "{{info-Lapses:}}",
    "{{info::Type}}": "{{info-Type:}}",
    "{{info::Nid}}": "{{info-Nid:}}",
    "{{info::Mod}}": "{{info-Mod:}}",
    "{{info::Usn}}": "{{info-Usn:}}",
    "{{info::Factor}}": "{{info-Factor:}}",
    "{{info::Ease}}": "{{info-Ease:}}",
    "{{info::Review?}}": "{{info-Review?:}}",
    "{{info::New?}}": "{{info-New?:}}",
    "{{info::Learning?}}": "{{info-Learning?:}}",
    "{{info::TodayLearning?}}": "{{info-TodayLearning?:}}",
    "{{info::DayLearning?}}": "{{info-DayLearning?:}}",
    "{{info::Young}}": "{{info-Young:}}",
    "{{info::Mature}}": "{{info-Mature:}}",
    "{{info::Options_Group_ID}}": "{{info-Options_Group_ID:}}",
    "{{info::Options_Group_Name}}": "{{info-Options_Group_Name:}}",
    "{{info::Ignore_answer_times_longer_than}}": "{{info-Ignore_answer_times_longer_than:}}",
    "{{info::Show_answer_time}}": "{{info-Show_answer_time:}}",
    "{{info::Auto_play_audio}}": "{{info-Auto_play_audio:}}",
    "{{info::When_answer_shown_replay_q}}": "{{info-When_answer_shown_replay_q:}}",
    "{{info::is_filtered_deck}}": "{{info-is_filtered_deck:}}",
    "{{info::deck_usn}}": "{{info-deck_usn:}}",
    "{{info::deck_mod_time}}": "{{info-deck_mod_time:}}",
    "{{info::new__steps_in_minutes}}": "{{info-new__steps_in_minutes:}}",
    "{{info::new__order_of_new_cards}}": "{{info-new__order_of_new_cards:}}",
    "{{info::new__cards_per_day}}": "{{info-new__cards_per_day:}}",
    "{{info::graduating_interval}}": "{{info-graduating_interval:}}",
    "{{info::easy_interval}}": "{{info-easy_interval:}}",
    "{{info::Starting_ease}}": "{{info-Starting_ease:}}",
    "{{info::bury_related_new_cards}}": "{{info-bury_related_new_cards:}}",
    "{{info::MaxiumReviewsPerDay}}": "{{info-MaxiumReviewsPerDay:}}",
    "{{info::EasyBonus}}": "{{info-EasyBonus:}}",
    "{{info::IntervalModifier}}": "{{info-IntervalModifier:}}",
    "{{info::MaximumInterval}}": "{{info-MaximumInterval:}}",
    "{{info::bur_related_reviews_until_next_day}}": "{{info-bur_related_reviews_until_next_day:}}",
    "{{info::lapse_learning_steps}}": "{{info-lapse_learning_steps:}}",
    "{{info::lapse_new_ivl}}": "{{info-lapse_new_ivl:}}",
    "{{info::lapse_min_ivl}}": "{{info-lapse_min_ivl:}}",
    "{{info::lapse_leech_threshold}}": "{{info-lapse_leech_threshold:}}",
    "{{info::lapse_leech_action}}": "{{info-lapse_leech_action:}}",
    "{{info::Date_Created}}": "{{info-Date_Created:}}",
    "{{info::allfields}}": "{{info-allfields:}}",
}


def update_for_these_templates_needed(ct):
    for old in newold.keys():
        if old in ct['qfmt'] or old in ct['afmt']:
            return True


def at_least_one_model_needs_to_be_updated():
    mids = mw.col.models.models.keys()
    for mid in mids:
        model = mw.col.models.get(mid)
        for cardtype in model['tmpls']:
            if update_for_these_templates_needed(cardtype):
                return True


def fix_models():
    for mid in mw.col.models.ids():
        model = mw.col.models.get(mid)
        for ct in model['tmpls']:
            for old, new in newold.items():
                ct['qfmt'] = ct['qfmt'].replace(old, new)
                ct['afmt'] = ct['afmt'].replace(old, new)
            mw.col.models.save(model)
    mw.col.models.flush()


addon_path = os.path.dirname(__file__)
user_files = os.path.join(addon_path, "user_files")
ran_2120_update = os.path.join(user_files, "ran_2120_template_update")


def update2120():
    if at_least_one_model_needs_to_be_updated():
        m = ("You use the add-on 'Additional Card Fields' and use syntax in your card templates "
             "that no longer works in Anki 2.1.20. For details see the description "
             "on https://ankiweb.net/shared/info/744725736. Adjust all your templates?")
        if askUser(m):
            fix_models()
    pathlib.Path(user_files).mkdir(parents=True, exist_ok=True) 
    pathlib.Path(ran_2120_update).touch()


old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 20)

if old_anki:
    from . import old_additional_card_fields
else:
    if not os.path.isfile(ran_2120_update):
        addHook("profileLoaded", update2120)
    from . import new_additional_card_fields
