from questions.models import Question
from teams.models import TeamsState
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def get_scoreboard_state():
    active_question = Question.objects.filter(is_active=True).first()
    
    if active_question:
        options_data = [
            {
                "id" : option.id,
                "text" : option.text if not option.hidden else "",
                "points" : option.points,
            }
            for option in active_question.options.all()
        ]
        question_payload = {
            "question" : active_question.text,
            "options" : sorted(options_data, key=lambda option: -option["points"]),
            "total_points" : active_question.points,
            "poll" : active_question.available_points
        }
    else:
        question_payload = {"question" : "No active question"}
        
    active_teams_state = TeamsState.objects.filter(is_active=True).first()
    if active_teams_state:
        teams_payload = {
            "left_team_mistakes" : active_teams_state.left_team_mistakes,
            "right_team_mistakes" : active_teams_state.right_team_mistakes
        }
    else:
        teams_payload = {
            "left_team_mistakes" : 0,
            "right_team_mistakes" : 0
        }
        
    return question_payload | teams_payload

def broadcast_scoreboard_update():
    channel_layer = get_channel_layer()
    payload = get_scoreboard_state()
        
    async_to_sync(channel_layer.group_send)(
        "scoreboard_group",
        {
            "type" : "scoreboard.update",
            "data" : payload
        }
    )