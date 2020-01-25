import os
import pathlib

from anki import version as anki_version
from anki.hooks import addHook
from aqt import mw
from aqt.utils import askUser


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    return fail


def wc(arg, val):
    config = mw.addonManager.getConfig(__name__)
    config[arg] = val
    mw.addonManager.writeConfig(__name__, config)


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


def at_least_one_model_needs_to_be_updated():
    mids = mw.col.models.models.keys()
    for mid in mids:
        model = mw.col.models.get(mid)
        for ct in model['tmpls']:
            if "{{info::" in ct['qfmt'] or "{{info::" in ct['afmt']:
                return True


def fix_models():
    mw.progress.start(immediate=True)
    for mid in mw.col.models.ids():
        model = mw.col.models.get(mid)
        for ct in model['tmpls']:
            for old, new in newold.items():
                ct['qfmt'] = ct['qfmt'].replace(old, new)
                ct['afmt'] = ct['afmt'].replace(old, new)
            mw.col.models.save(model)
    mw.col.models.flush()
    mw.progress.finish()


def update2120():
    if at_least_one_model_needs_to_be_updated():
        m = ("You use the add-on 'Additional Card Fields' and use syntax in your card templates "
             "like '{{info::Due}}', '{{info::Factor}}', etc. that no longer works in Anki 2.1.20. "
             "Because of technical changes in Anki 2.1.20 you need to modify the templates "
             "and use '{{info-Due:}}', '{{info-Factor:}}', etc. "
             "If you don't update your templates you will get an error message instead of seeing "
             "your card contents when you review a card that has the old syntax in its template.\n\n"
             "For details see the description on https://ankiweb.net/shared/info/744725736.\n\n"
             "This add-on can also automatically update all your templates now. Proceed?\n\n"
             "If you cancel now and want to update your templates later you'll have to adjust "
             "the config of this add-on and enable the setting 'show 2.1.20 update message "
             "on next start' and restart Anki.")
        if askUser(m):
            fix_models()
    wc("show 2.1.20 update message on next start", False)


old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 20)

if old_anki:
    from . import old_additional_card_fields
else:
    if gc("show 2.1.20 update message on next start", True):
        addHook("profileLoaded", update2120)
    from . import new_additional_card_fields
