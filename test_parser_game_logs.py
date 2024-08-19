import unittest
from collections import defaultdict

from parser_game_logs import parse_log_file, print_report

class TestQuakeLogParser(unittest.TestCase):

    def setUp(self):
        # Mock log data simulating various scenarios
        # In real life we should split every scenario
        self.mock_log_data = """
            0:00 InitGame:
            0:25 ClientConnect: 2
            0:25 ClientUserinfoChanged: 2 
            0:27 ClientUserinfoChanged: 2 
            0:27 ClientBegin: 2
            0:29 Item: 2 weapon_rocketlauncher
            0:35 Item: 2 item_armor_shard
            0:35 Item: 2 item_armor_shard
            0:35 Item: 2 item_armor_shard
            0:35 Item: 2 item_armor_combat
            0:38 Item: 2 item_armor_shard
            0:38 Item: 2 item_armor_shard
            0:38 Item: 2 item_armor_shard
            0:55 Item: 2 item_health_large
            0:56 Item: 2 weapon_rocketlauncher
            0:57 Item: 2 ammo_rockets
            0:59 ClientConnect: 3
            0:59 ClientUserinfoChanged: 3 
            1:01 ClientUserinfoChanged: 3 
            1:01 ClientBegin: 3
            1:02 Item: 3 weapon_rocketlauncher
            1:04 Item: 2 item_armor_shard
            1:04 Item: 2 item_armor_shard
            1:04 Item: 2 item_armor_shard
            1:06 ClientConnect: 4
            1:06 ClientUserinfoChanged: 4 
            1:08 Kill: 3 2 6: Isgalamido Silva killed Mocinha by MOD_ROCKET
            1:08 ClientUserinfoChanged: 4 
            1:08 ClientBegin: 4
            1:10 Item: 3 item_armor_shard
            1:10 Item: 3 item_armor_shard
            1:10 Item: 3 item_armor_shard
            1:10 Item: 3 item_armor_combat
            1:11 Item: 4 weapon_shotgun
            1:11 Item: 4 ammo_shells
            1:16 Item: 4 item_health_large
            1:18 Item: 4 weapon_rocketlauncher
            1:18 Item: 4 ammo_rockets
            1:26 Kill: 1022 4 22: <world> killed Zeh by MOD_TRIGGER_HURT
            1:26 ClientUserinfoChanged: 2 
            1:26 Item: 3 weapon_railgun
            1:29 Item: 2 weapon_rocketlauncher
            1:29 Item: 3 weapon_railgun
            1:32 Item: 3 weapon_railgun
            1:32 Kill: 1022 4 22: <world> killed Zeh by MOD_TRIGGER_HURT
            1:35 Item: 2 item_armor_shard
            1:35 Item: 2 item_armor_shard
            1:35 Item: 2 item_armor_shard
            1:35 Item: 3 weapon_railgun
            1:38 Item: 2 item_health_large
            1:38 Item: 3 weapon_railgun
            1:41 Kill: 1022 2 19: <world> killed Dono da Bola by MOD_FALLING
            1:41 Item: 3 weapon_railgun
            1:43 Item: 2 ammo_rockets
            1:44 Item: 2 weapon_rocketlauncher
            1:46 Item: 2 item_armor_shard
            1:47 Item: 2 item_armor_shard
            1:47 Item: 2 item_armor_shard
            1:47 ShutdownGame:
        """
        self.expected_games = {
            "game_1":{
                "total_kills": 4,
                "players": ["Isgalamido Silva", "Zeh", "Mocinha", "Dono da Bola"],
                "kills": {
                    "Isgalamido Silva": 1, 
                    "Zeh": 0, 
                    "Dono da Bola": 0
                }
            }
        }
        self.expected_player_ranking = {
            "Isgalamido Silva": 1,
            "Zeh": 0,
            "Dono da Bola": 0
        }

    def test_parse_log_file_happy_path(self):
        # Write the mock data to a temporary file
        log_file_path = 'mock_logs.log'
        with open(log_file_path, 'w') as file:
            file.write(self.mock_log_data)

        games, player_ranking = parse_log_file(log_file_path)

        # Convert defaultdict to regular dict for comparison
        games = {k: dict(v) if isinstance(v, defaultdict) else v for k, v in games.items()}
        
        # Assert that the parsed game data matches the expected data
        self.assertEqual(sorted(games['game_1']['players']), sorted(self.expected_games['game_1']['players']))

        # Assert that the player ranking matches the expected ranking
        self.assertEqual(player_ranking, self.expected_player_ranking)

    def test_print_report_happy_path(self):
        report = print_report(self.expected_games, self.expected_player_ranking)

        # Ensure report is not None
        self.assertIsNotNone(report, "The report is None, expected a string.")

        expected_report = """
game_1:
  total_kills: 4
  players: ['Isgalamido Silva', 'Zeh', 'Mocinha', 'Dono da Bola']
  kills: {'Isgalamido Silva': 1, 'Zeh': 0, 'Dono da Bola': 0}
Player Ranking:
Isgalamido Silva: 1 kills
Zeh: 0 kills
Dono da Bola: 0 kills            
        """

        # Compare reports, ignoring leading/trailing whitespaces and newlines
        self.assertEqual(report.strip(), expected_report.strip())

    def test_world_kill_deduction(self):
        # Mock log data to test kill deduction by <world>
        mock_log_data_world_kill = """
            21:00 InitGame: 
            21:01 Kill: 1022 2 22: <world> killed Isgalamido Silva by MOD_TRIGGER_HURT
            21:01 Kill: 1022 2 22: <world> killed Isgalamido Silva by MOD_TRIGGER_HURT
            21:02 ShutdownGame:
        """
        expected_games_world_kill = {
            "game_1": {
                "total_kills": 2,
                "players": ["Isgalamido Silva"],
                "kills": {
                    "Isgalamido Silva": 0  # Kill count should not go below 0
                }
            }
        }
        expected_player_ranking_world_kill = {
            "Isgalamido Silva": 0
        }

        # Write the mock data to a temporary file
        log_file_path = 'mock_logs_world.log'
        with open(log_file_path, 'w') as file:
            file.write(mock_log_data_world_kill)

        games, player_ranking = parse_log_file(log_file_path)

        # Convert defaultdict to regular dict for comparison
        games = {k: dict(v) if isinstance(v, defaultdict) else v for k, v in games.items()}

        self.assertEqual(games, expected_games_world_kill)
        self.assertEqual(player_ranking, expected_player_ranking_world_kill)

if __name__ == '__main__':
    unittest.main()
