from app import form_response 

class  NotANumber(Exception):
    def __init__(self, message="Values entered are not Numerical"):
        self.message = message
        super().__init__(self.message)

input_data = {
    "incorrect_values": 
    {"week_of_season": 3, 
    "home_users": 4, 
    "away_users": 'as', 
    "concurrent_games": 1, 
    "last_5_handle_all": 'ab', 
    "home_team_popularity": 'as', 
    "away_team_popularity": 12, 
    "time_slot_fri": 1, 
    "time_slot_mon_early": 'ab',
    "time_slot_mon_late": 1, 
    "time_slot_mon_mid": 'ab',
    "time_slot_odd_days": 1, 
    "time_slot_sun": 'ab',
    "time_slot_tues": 'ab',
    },

    "correct_values": 
    {"week_of_season": 3, 
    "home_users": 4, 
    "away_users": 123, 
    "concurrent_games": 1, 
    "last_5_handle_all": 45764, 
    "home_team_popularity": 0.95, 
    "away_team_popularity": 0.12, 
    "time_slot_fri": 1, 
    "time_slot_mon_early": 0,
    "time_slot_mon_late": 0, 
    "time_slot_mon_mid": 0,
    "time_slot_odd_days": 0, 
    "time_slot_sun": 0,
    "time_slot_tues": 0,
    }
}

def test_form_response_incorrect_values(data=input_data["incorrect_values"]):
    res=form_response(data)
    assert res == NotANumber().message