from collections import defaultdict

def parse_log_file(filepath):
    games = {}
    player_ranking = defaultdict(int)
    current_game = None

    with open(filepath, 'r') as file:
        for line in file:
            if 'InitGame' in line:
                # Start a new game
                current_game = f"game_{len(games) + 1}"
                games[current_game] = {
                    "total_kills": 0,
                    "players": set(),
                    "kills": defaultdict(int)
                }
            elif 'Kill' in line:
                # Process kills
                # parts = line.split()
                # killer = parts[5] # Killer Name
                # victim_start_idx = line.index("killed") + len("killed") + 1
                # victim_end_idx = line.index("by") - 1
                # victim = line[victim_start_idx:victim_end_idx].strip() # Victim Name

                parts = line.split()
                killer_start_idx = line.index(parts[5])
                killer_end_idx = line.index("killed") - 1
                killer = line[killer_start_idx:killer_end_idx].strip()
                
                victim_start_idx = line.index("killed") + len("killed") + 1
                victim_end_idx = line.index("by") - 1
                victim = line[victim_start_idx:victim_end_idx].strip()

                if current_game:
                    games[current_game]['total_kills'] += 1

                    if killer != '<world>':
                        games[current_game]['players'].add(killer)
                        games[current_game]['kills'][killer] += 1
                        player_ranking[killer] += 1

                    games[current_game]['players'].add(victim)
                    
                    if killer == '<world>':
                        # Only subtract if killed by <world>, and ensure minimum kills is 0
                        if games[current_game]['kills'][victim] > 0:
                            games[current_game]['kills'][victim] -= 1
                        player_ranking[victim] = max(0, player_ranking[victim] - 1)

            elif 'ShutdownGame' in line and current_game:
                # Convert set of players to list and kills defaultdict to dict
                games[current_game]['players'] = list(games[current_game]['players'])
                games[current_game]['kills'] = dict(games[current_game]['kills'])
                current_game = None

    return games, dict(player_ranking)

def print_report(games, player_ranking):
    report_lines = []
    for game, data in games.items():
        report_lines.append(f"{game}:")
        report_lines.append(f"  total_kills: {data['total_kills']}")
        report_lines.append(f"  players: {data['players']}")
        
        # Convert defaultdict to dict before adding to report
        kills = dict(data['kills'])
        report_lines.append(f"  kills: {kills}")
    
    report_lines.append("Player Ranking:")
    
    # Sorts the player ranking by the number of kills
    sorted_ranking = sorted(player_ranking.items(), key=lambda item: item[1], reverse=True)

    for player, kills in sorted_ranking:
        report_lines.append(f"{player}: {kills} kills")
    
    # Join all lines into a single report string
    report_string = "\n".join(report_lines)
    
    # Print the report
    print(report_string)
    
    # Return the report as string for testing purposes
    return report_string

if __name__ == "__main__":
    log_file_path = "logs.log"  # Path to your log file
    games, player_ranking = parse_log_file(log_file_path)
    print_report(games, player_ranking)
