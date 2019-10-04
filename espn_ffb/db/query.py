from collections import namedtuple
from espn_ffb.db.model.champions import Champions
from espn_ffb.db.model.matchups import Matchups
from espn_ffb.db.model.owners import Owners
from espn_ffb.db.model.records import Records
from espn_ffb.db.model.sackos import Sackos
from espn_ffb.db.model.teams import Teams
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import Sequence


class Query:
    def __init__(self, db):
        self.db = db

    def get_champions(self):
        """
        Select champions.

        :return: list of champions
        """
        champions = self.db.session.query(Champions, Owners) \
            .join(Owners, Champions.owner_id == Owners.id) \
            .order_by(desc(Champions.year)) \
            .all()

        return champions

    def get_distinct_matchup_team_ids(self, year: int):
        distinct_matchup_team_ids = dict()
        matchups = self.get_matchups(year)
        for matchup in matchups:
            if matchup.matchup_id not in distinct_matchup_team_ids:
                distinct_matchup_team_ids[matchup.matchup_id] = {matchup.team_id}
            else:
                if (matchup.opponent_team_id is None) or (
                        matchup.opponent_team_id not in distinct_matchup_team_ids.get(matchup.matchup_id)):
                    distinct_matchup_team_ids[matchup.matchup_id].add(matchup.team_id)

        return distinct_matchup_team_ids

    def get_h2h_record_current(self, matchups, year, week):
        Record = namedtuple('Record', ['wins', 'losses'])
        h2h_record = list()
        for m in matchups:
            wins, losses = 0, 0
            h2h_history = [h2h for h2h in self.get_matchup_history(m.owner_id, m.opponent_owner_id, False) if
                           not (h2h.year == year and h2h.matchup_id == week)]

            for h2h in h2h_history:
                if h2h.is_win:
                    wins += 1
                else:
                    losses += 1

            h2h_record.append(Record(wins, losses))

        return h2h_record

    def get_h2h_records(self, owner_id, is_playoffs):
        COLUMN_NAMES = ['opponent_name', 'wins', 'losses']
        Record = namedtuple('H2HRecord', COLUMN_NAMES)

        query = f"""
        select
          record.opponent_name as opponent_name,
          sum(record.wins) as wins,
          sum(record.losses) as losses
        from
          (
            select
              m.year,
              m.matchup_id,
              (
                select
                  concat_ws(' ', o.first_name, o.last_name)
                from
                  owners o
                where
                  o.id = m.owner_id
              ) as owner_name,
              m.owner_id,
              (
                select
                  concat_ws(' ', o.first_name, o.last_name)
                from
                  owners o
                where
                  o.id = m.opponent_owner_id
              ) as opponent_name,
              m.opponent_owner_id,
              case m.is_win when true then 1 else 0 end as wins,
              case m.is_loss when true then 1 else 0 end as losses
            from
              matchups m
            where
              m.is_playoffs = {is_playoffs}
              and not m.is_consolation
              and m.owner_id = '{owner_id}'
              and m.opponent_owner_id is not null
            group by
              m.year,
              m.matchup_id,
              owner_name,
              m.owner_id,
              opponent_name,
              m.opponent_owner_id,
              wins,
              losses
          ) as record
        group by
          record.opponent_name
        order by
          opponent_name
        """

        return [Record(**r) for r in self.db.engine.execute(query)]

    def get_matchup_history(self, owner_id, opponent_owner_id, is_playoffs):
        matchups = self.db.session.query(Matchups) \
            .filter_by(owner_id=owner_id,
                       opponent_owner_id=opponent_owner_id,
                       is_playoffs=is_playoffs,
                       is_pending=False,
                       is_consolation=False) \
            .order_by(desc(Matchups.year), Matchups.matchup_id) \
            .all()
        return matchups

    def get_matchups(self, year: int) -> Sequence[Matchups]:
        """
        Select matchups for a given year.

        :param year: the year
        :return: list of matchups
        """
        matchups = self.db.session.query(Matchups) \
            .filter_by(year=year) \
            .order_by(Matchups.matchup_id, Matchups.team_id) \
            .all()
        return matchups

    def get_owners(self):
        return self.db.session.query(Owners).all()

    def get_records(self, year: int) -> Sequence[Records]:
        """
        Select records for a given year.

        :param year: the year
        :return: list of records
        """
        records = self.db.session.query(Records).filter_by(year=year).all()
        return records

    def get_sacko_current(self):
        sacko = self.db.session.query(Sackos) \
            .order_by(desc(Sackos.year)) \
            .first()
        return sacko

    def get_standings(self, year: int):
        COLUMN_NAMES = ["owner_id", "wins", "losses", "win_percentage", "points_for", "points_against", "avg_points_for",
                        "avg_points_against", "championships", "sackos"]
        Record = namedtuple('Standings', COLUMN_NAMES)

        query = f"""
        select 
          r.owner_id as owner_id,
          r.wins as wins,
          r.losses as losses,
          round(r.wins::decimal/(r.wins + r.losses), 4) as win_percentage,
          r.points_for as points_for,
          r.points_against as points_against,
          round(r.points_for/(r.wins + r.losses), 2) as avg_points_for,
          round(r.points_for/(r.wins + r.losses), 2) as avg_points_against,
          (select count(1) from champions where owner_id = r.owner_id and year = r.year) as championships,
          (select count(1) from sackos where owner_id = r.owner_id and year = r.year) as sackos
        from 
          records r
        where 
          r.year = {year}
        group by
          r.year,
          r.owner_id,
          r.wins,
          r.losses,
          r.points_for,
          r.points_against
        order by
          win_percentage desc,
          points_for desc
        """

        return [Record(**r) for r in self.db.engine.execute(query)]

    def get_standings_overall(self):
        COLUMN_NAMES = ["owner_id", "wins", "losses", "win_percentage", "points_for", "points_against", "avg_points_for",
                        "avg_points_against", "championships", "sackos"]
        Record = namedtuple('Standings', COLUMN_NAMES)

        query = f"""
        select
          r.owner_id as owner_id,
          sum(r.wins) as wins,
          sum(r.losses) as losses,
          round(sum(r.wins)::decimal/(sum(r.wins)+sum(r.losses)), 4) as win_percentage,
          sum(r.points_for) as points_for,
          sum(r.points_against) as points_against,
          round(sum(r.points_for)/(sum(r.wins)+sum(r.losses)), 2) as avg_points_for,
          round(sum(r.points_against)/(sum(r.wins)+sum(r.losses)), 2) as avg_points_against,
          (select count(1) from champions where owner_id = r.owner_id) as championships,
          (select count(1) from sackos where owner_id = r.owner_id) as sackos
        from
          records r
        group by
          r.owner_id
        order by
          win_percentage desc,
          avg_points_for desc
        """

        return [Record(**r) for r in self.db.engine.execute(query)]

    def get_team_id_to_record(self, year, week):
        team_id_to_record = dict()
        Record = namedtuple('Record', ['wins', 'losses'])
        matchups = self.get_matchups(year)
        for m in matchups:
            if m.team_id in team_id_to_record:
                r = team_id_to_record.get(m.team_id)
            else:
                r = Record(0, 0)
                team_id_to_record[m.team_id] = r

            if m.matchup_id < week:
                if m.team_score > m.opponent_team_score:
                    team_id_to_record[m.team_id] = Record(r.wins + 1, r.losses)
                if m.team_score < m.opponent_team_score:
                    team_id_to_record[m.team_id] = Record(r.wins, r.losses + 1)

        return team_id_to_record

    def get_team_id_to_team_name(self, year):
        records = self.get_teams(year)
        return dict((record.id, record.location + " " + record.nickname) for record in records)

    def get_teams(self, year: int):
        """
        Select teams for a given year.

        :param year: the year
        :return: list of teams
        """
        teams = self.db.session.query(Teams).filter_by(year=year).all()
        return teams

    def get_win_streak_by_year(self, matchups, year, week):
        win_streaks = list()
        WinStreak = namedtuple('WinStreak', ['streak', 'streak_owner'])

        for m in matchups:
            streak, streak_owner, streak_type = 0, None, None
            h2h_history = [h2h for h2h in self.get_matchup_history(m.owner_id, m.opponent_owner_id, False) if
                           not (h2h.year == year and h2h.matchup_id == week)]

            for h2h in h2h_history:
                if streak == 0:
                    streak_type = h2h.is_win
                    streak_owner = m.team_id if streak_type else m.opponent_team_id

                if h2h.is_win != streak_type:
                    streak_owner = m.team_id if streak_type else m.opponent_team_id
                    break

                streak += 1
            win_streaks.append(WinStreak(streak, streak_owner))

        return win_streaks

    def upsert_matchups(self, matchups):
        for m in matchups:
            statement = pg_insert(Matchups) \
                .values(**m.as_dict()) \
                .on_conflict_do_update(constraint=Matchups.PKEY_NAME, set_=m.props_dict())
            self.db.session.execute(statement)
        self.db.session.commit()

    def upsert_records(self, records):
        for record in records:
            statement = pg_insert(Records) \
                .values(**record.as_dict()) \
                .on_conflict_do_update(constraint=Records.PKEY_NAME, set_=record.props_dict())
            self.db.session.execute(statement)
        self.db.session.commit()

    def upsert_teams(self, teams):
        for team in teams:
            statement = pg_insert(Teams) \
                .values(**team.as_dict()) \
                .on_conflict_do_update(constraint=Teams.PKEY_NAME, set_=team.props_dict())
            self.db.session.execute(statement)
        self.db.session.commit()
