import pandas as pd
import random
import os

def generate_question(player, team, question_type):
    switch = {
        1: f'Which Serie A team(s) has {player} played for?',
        2: f'When did {player} debut in Serie A?',
        3: f'When did {player} play his final Seria A game?',
        4: f'How many Serie A goals did {player} score?',
        5: f'How many goals per game did {player} average in Serie A?',
        6: f'How many goals did {player} score for {team} in Serie A?',
        7: f'How many matches did {player} play for {team} in Serie A?',
        8: f'For which team(s) did {player} score the most goals in Serie A?',
        9: f'For which team(s) did {player} register the most appearances in Serie A?',
        10: f'How many Serie A matches did {player} play?',
    }
    return switch[question_type]

def read_goals(df, player):
    return df[df['Player'] == player]['Goals'].values[0]

def read_apps(df, player):
    return df[df['Player'] == player]['Apps'].values[0]

def read_club_stats(df, player):
    #The data has some entries ending in a comma. The comma needs to be removed
    club_stats = df[df['Player'] == player]['Club(s) (goals/apps)'].values[0].rstrip(',')
    #Correct missing ')'
    club_stats = ', '.join([x + ')' if x[-1] != ')' and '(' in x else x for x in club_stats.split(', ')])
    if '(' in club_stats:
        return club_stats
    return f'{club_stats} ({read_goals(df, player)}/{read_apps(df, player)})'

def read_debut(df, player):
    return df[df['Player'] == player]['First'].values[0]

def read_final_game(df, player):
    return df[df['Player'] == player]['Last'].values[0]

def read_ratio(df, player):
    return df[df['Player'] == player]['Ratio'].values[0]

def extract_teams(clubs_stats):
    return [team.split('(')[0].strip() for team in clubs_stats.rstrip(',').split(',')] #Removing the final comma misplaced in some strings, hence the rstrip

def group_club_stats(df, player):
    club_stats = read_club_stats(df, player)
    player_teams = extract_teams(club_stats)
    goals_for_team = [x.split('/')[0] for x in club_stats.split('(')[1:]]
    matches_for_team = [x.split('/')[-1] for x in club_stats.split(')')][:-1]
    stats_df = pd.DataFrame({'Team': player_teams, 'Goals': [int(x) for x in goals_for_team], 'Matches': [int(x) for x in matches_for_team]})
    return(stats_df)

def find_goals_for_team(df, player, team):
    stats_df = group_club_stats(df, player)
    if team not in list(stats_df['Team']):
        return 0
    return stats_df[stats_df['Team'] == team]['Goals'].values[0]

def find_matches_for_team(df, player, team):
    stats_df = group_club_stats(df, player)
    if team not in list(stats_df['Team']):
        return 0
    return stats_df[stats_df['Team'] == team]['Matches'].values[0]

def join_with_comma(input_list):
    if len(input_list) < 3:
        return ' and '.join(input_list)
    return ', '.join(input_list[:-1]) + ' and ' + input_list[-1]

def find_max_club_stats(stats_df, column):
    max_value = stats_df[column].max()
    max_value_rows = stats_df[stats_df[column] == max_value]
    max_clubs = list(max_value_rows['Team'])
    return join_with_comma(max_clubs)

def find_max_goals_team(df, player):
    stats_df = group_club_stats(df, player)
    return find_max_club_stats(stats_df, 'Goals')

def find_max_apps_team(df, player):
    stats_df = group_club_stats(df, player)
    return find_max_club_stats(stats_df, 'Goals')

def extract_player_teams(df, player):
    return extract_teams(read_club_stats(df, player))

def read_player_teams(df, player):
    return join_with_comma(extract_player_teams(df, player))
    
def extract_all_teams(df):
    teams = []
    club_stats = list(df['Club(s) (goals/apps)'])
    for x in club_stats:
        teams += extract_teams(x)
    return list(set(teams))

def find_correct_answer(df, player, team, question_type):
    switch = {
        1: lambda df, player: read_player_teams(df, player),
        2: lambda df, player: read_debut(df, player),
        3: lambda df, player: read_final_game(df, player),
        4: lambda df, player: read_goals(df, player),
        5: lambda df, player: read_ratio(df, player),
        6: lambda df, player, team: find_goals_for_team(df, player, team),
        7: lambda df, player, team: find_matches_for_team(df, player, team),
        8: lambda df, player: find_max_goals_team(df, player),
        9: lambda df, player: find_max_apps_team(df, player),
        10: lambda df, player: read_apps(df, player)
    }
    if question_type in [6, 7]:
        return switch[question_type](df, player, team)
    return switch[question_type](df, player)

def split_from_comma(input_str):
    return input_str.replace(' and ', ', ').split(', ')

def read_player_teamsF (teams, correct_answer):
    correct_teams = split_from_comma(correct_answer)
    answers = [correct_teams]
    extra_teams = random.sample(list(set(teams) - set(correct_teams)), len(correct_teams) + 1)
    used_teams = correct_teams + extra_teams
    while True:
        sorted_answers = [sorted(x) for x in answers]
        answer = random.sample(used_teams, random.randint(1, len(used_teams)))
        if sorted(answer) not in sorted_answers:
            answers.append(answer)
        if len(answers) == 5:
            break
    answers = [join_with_comma(x) for x in answers]
    return answers

def read_countF (correct_answer, default_var):
    answers = [correct_answer]
    default_var  = min(correct_answer + 15, default_var)
    start_count = random.randint(max(correct_answer - default_var, 1), correct_answer + default_var // 2 - 5)
    stop_count = random.randint(start_count + 5, min (correct_answer + default_var, 2024))
    while True:
        answer = random.randint(start_count, stop_count)
        if answer not in answers:
            answers.append(answer)
        if len(answers) == 5:
            break
    return answers

def read_yearF (correct_answer):
    return read_countF(correct_answer, 5)

def read_goalsF (correct_answer):
    return read_countF(correct_answer, 40)

def read_appsF (correct_answer):
    return read_countF(correct_answer, 100)

def read_ratioF(correct_answer, default_var = 0.2):
    answers = [correct_answer]
    start_ratio = round(random.uniform(max(correct_answer - default_var, 0), min(correct_answer + default_var / 2, 0.95)), 2)
    stop_ratio = round(random.uniform(start_ratio + 0.05, min(correct_answer + default_var, 1)), 2)                
    while True:
        answer = round(random.uniform(start_ratio, stop_ratio), 2)
        if answer not in answers:
            answers.append(answer)
        if len(answers) == 5:
            break
    return answers

def find_teamF(teams, correct_answer):
    correct_teams = split_from_comma(correct_answer)
    answers = [correct_teams]
    extra_teams = random.sample(list(set(teams) - set(correct_teams)), len(correct_teams) + 5)
    used_teams = correct_teams + extra_teams
    while True:
        sorted_answers = [sorted(x) for x in answers]
        sample_size = random.choices([1, 2, 3], weights = [100, 10, 1])[0]
        answer = random.sample(used_teams, sample_size)
        if sorted(answer) not in sorted_answers:
            answers.append(answer)
        if len(answers) == 5:
            break
    answers = [join_with_comma(x) for x in answers]
    return answers
    
def generate_choices(teams, correct_answer, question_type):
    switch = {
        1: lambda teams, correct_answer: read_player_teamsF(teams, correct_answer),
        2: lambda correct_answer: read_yearF(correct_answer),
        3: lambda correct_answer: read_yearF(correct_answer),
        4: lambda correct_answer: read_goalsF(correct_answer),
        5: lambda correct_answer: read_ratioF(correct_answer),
        6: lambda correct_answer: read_goalsF(correct_answer),
        7: lambda correct_answer: read_appsF(correct_answer),
        8: lambda teams, correct_answer: find_teamF(teams, correct_answer),
        9: lambda teams, correct_answer: find_teamF(teams, correct_answer),
        10: lambda correct_answer: read_appsF(correct_answer)
    }
    
    if question_type in [1, 8, 9]:
        return switch[question_type](teams, correct_answer)
    return switch[question_type](correct_answer)

def generate_questions(df, n_questions):
    players = list(df['Player'])
    teams = extract_all_teams(df)
    questions = []    
    for i in range(n_questions):
        question_type = random.randint(1, 10)
        player = random.choice(players)
        player_teams = extract_player_teams(df, player)
        extra_team = random.choice(list(set(teams) - set(player_teams)))
        team = random.choice(player_teams + [extra_team])
        correct_answer = find_correct_answer(df, player, team, question_type)
        choices = generate_choices(teams, correct_answer, question_type)
        random.shuffle(choices)
        letter = ['A', 'B', 'C', 'D', 'E'][choices.index(correct_answer)]
        questions.append([generate_question(player, team, question_type)] + choices + [letter])
    questions = pd.DataFrame(questions, columns = ['Question', 'A', 'B', 'C', 'D', 'E', 'Correct'])
    if not os.path.exists('Output'):
        os.makedirs('Output')
    questions.to_csv('Output/quiz.csv')
    return questions
    
def main():
    df = pd.read_csv('Data/serieadata.csv')
    n_questions = 20
    generate_questions(df, n_questions)
    teams = extract_all_teams(df)

if __name__ == '__main__':
    main()
